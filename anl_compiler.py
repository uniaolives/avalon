# anl_compiler.py
import json
import os
import sys
import re
import ast
import numpy as np
from arkhe_language_spec import Hypergraph, Node, Handover, StateSpace, Protocol

def hg_to_air(hg: Hypergraph) -> dict:
    """
    Serializa um objeto Hypergraph para o formato AIR (JSON).
    """
    return {
        "air_version": "0.1.0",
        "hypergraph": {
            "id": hg.name,
            "nodes": [
                {
                    "id": n.id,
                    "state_space": {
                        "dimension": n.state_space.dimension,
                        "topology": n.state_space.topology,
                        "algebra": n.state_space.algebra
                    },
                    "initial_state": n.current_state.tolist() if isinstance(n.current_state, np.ndarray) else n.current_state,
                    "dynamics": str(n.internal_dynamics),
                    "attributes": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in getattr(n, 'attributes', {}).items()},
                    "observables": {k: str(v) for k, v in n.observables.items()}
                } for n in hg.nodes.values()
            ],
            "handovers": [
                {
                    "id": h.id,
                    "source": h.source.id,
                    "target": h.target.id,
                    "protocol": h.protocol.value,
                    "map": str(h.map_state),
                    "condition": getattr(h, 'condition', None),
                    "effects": getattr(h, 'effects', None),
                    "latency": h.latency,
                    "bandwidth": h.bandwidth,
                    "fidelity": h.fidelity,
                    "entanglement": h.entanglement
                } for h in hg.handovers.values()
            ]
        }
    }

def extract_nested_block(code, start_pos):
    count = 1
    i = start_pos
    while i < len(code) and count > 0:
        if code[i] == '{':
            count += 1
        elif code[i] == '}':
            count -= 1
        i += 1
    if count == 0:
        return code[start_pos:i-1], i
    return None, i

def compile_anl_v02(code: str) -> Hypergraph:
    """
    Parser experimental para a sintaxe ANL 0.2.
    """
    hg = Hypergraph("ANL-02-Model")

    # Remove comentários
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # Nós
    node_pattern = re.compile(r'node\s+(\w+)\s*\{')
    pos = 0
    while True:
        match = node_pattern.search(code, pos)
        if not match: break

        node_id = match.group(1)
        body, next_pos = extract_nested_block(code, match.end())
        pos = next_pos

        if body:
            attr_dict = {}
            attr_match = re.search(r'attributes\s*\{', body)
            if attr_match:
                attr_body, _ = extract_nested_block(body, attr_match.end())
                if attr_body:
                    for line in attr_body.strip().split(';'):
                        line = line.strip()
                        if not line or '=' not in line: continue

                        decl, val = line.split('=', 1)
                        decl_parts = decl.strip().split()
                        if len(decl_parts) >= 2:
                            attr_name = decl_parts[1]
                            attr_val = val.strip()
                            try:
                                # Tenta avaliar como Python literal
                                attr_dict[attr_name] = ast.literal_eval(attr_val)
                            except:
                                attr_dict[attr_name] = attr_val

            dynamics_str = None
            dynamics_match = re.search(r'dynamics\s*\{', body)
            if dynamics_match:
                dynamics_body, _ = extract_nested_block(body, dynamics_match.end())
                dynamics_str = dynamics_body.strip() if dynamics_body else None

            node = Node(node_id, StateSpace.euclidean(0), attributes=attr_dict, internal_dynamics=dynamics_str)
            hg.add_node(node)

    # Handovers
    handover_pattern = re.compile(r'handover\s+(\w+)\s*\(([^)]+)\)\s*\{')
    pos = 0
    while True:
        match = handover_pattern.search(code, pos)
        if not match: break

        h_id = match.group(1)
        params = match.group(2)
        body, next_pos = extract_nested_block(code, match.end())
        pos = next_pos

        # Extrai os tipos como IDs de nós (ex: "Coelho c, Grama g" -> ["Coelho", "Grama"])
        param_types = [p.strip().split()[0] for p in params.split(',')]

        if len(param_types) >= 2:
            src_name, dst_name = param_types[0], param_types[1]
            src = hg.nodes.get(src_name, Node(src_name, StateSpace.euclidean(0)))
            dst = hg.nodes.get(dst_name, Node(dst_name, StateSpace.euclidean(0)))

            condition = None
            cond_match = re.search(r'condition:\s*([^;]+);', body)
            if cond_match:
                condition = cond_match.group(1).strip()

            effects = None
            effects_match = re.search(r'effects\s*\{', body)
            if effects_match:
                effects_body, _ = extract_nested_block(body, effects_match.end())
                effects = effects_body.strip() if effects_body else None

            h = Handover(h_id, src, dst, Protocol.CREATIVE, condition=condition, effects=effects)
            hg.add_handover(h)

    return hg

def compile_anl_file(filename: str) -> dict:
    """
    Compila um arquivo .arkhe ou .anl em Arkhe Intermediate Representation (AIR).
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Arquivo {filename} não encontrado.")

    with open(filename, "r") as f:
        code = f.read()

    # Detecta se é sintaxe v02 (presença de 'node' seguido de '{')
    if re.search(r'node\s+\w+\s*\{', code):
        hg = compile_anl_v02(code)
    else:
        # Prepara o namespace para Python DSL
        namespace = {
            'Hypergraph': Hypergraph,
            'Node': Node,
            'Handover': Handover,
            'StateSpace': StateSpace,
            'Protocol': Protocol,
            'np': np,
        }

        try:
            exec(code, namespace)
        except Exception as e:
            raise RuntimeError(f"Erro ao executar o código ANL (Python DSL): {e}")

        # Procura por instâncias de Hypergraph no namespace
        hg = namespace.get('hypergraph')
        if hg is None:
            for val in namespace.values():
                if isinstance(val, Hypergraph):
                    hg = val
                    break

    if hg is None:
        raise ValueError("Arquivo ANL deve definir uma instância de 'Hypergraph' ou conter definições de 'node'")

    return hg_to_air(hg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 anl_compiler.py <arquivo.anl|arquivo.arkhe>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = re.sub(r'\.(anl|arkhe)$', '.air.json', input_file)
    if output_file == input_file:
        output_file += ".air.json"

    try:
        air = compile_anl_file(input_file)
        with open(output_file, "w") as f:
            json.dump(air, f, indent=2)
            f.write("\n")
        print(f"✅ Compilação concluída: {output_file}")
    except Exception as e:
        print(f"❌ Erro na compilação: {e}")
        sys.exit(1)
