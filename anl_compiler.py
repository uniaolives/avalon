# anl_compiler.py
import json
import os
import sys
import re
import ast
import numpy as np
from arkhe_language_spec import Hypergraph, Node, Handover, StateSpace, Protocol, Constraint

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
                    "parent_id": getattr(n, 'parent_id', None),
                    "state_space": {
                        "dimension": n.state_space.dimension,
                        "topology": n.state_space.topology,
                        "algebra": n.state_space.algebra
                    },
                    "initial_state": n.current_state.tolist() if isinstance(n.current_state, np.ndarray) else n.current_state,
                    "dynamics": str(n.internal_dynamics),
                    "attributes": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in getattr(n, 'attributes', {}).items()},
                    "functions": getattr(n, 'functions', {}),
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
            ],
            "enums": hg.enums,
            "namespaces": hg.namespaces,
            "dynamics": hg.dynamics,
            "constraints": [
                {
                    "id": c.id,
                    "check": c.check,
                    "mode": c.mode,
                    "measurement": c.measurement,
                    "on_violation": c.on_violation
                } for c in hg.constraints.values()
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

def split_by_top_level_semicolon(text):
    parts = []
    current = []
    depth = 0
    for char in text:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1

        if char == ';' and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    last = "".join(current).strip()
    if last:
        parts.append(last)
    return parts

def compile_anl_v02(code: str) -> Hypergraph:
    """
    Parser experimental para a sintaxe ANL 0.2.
    """
    hg = Hypergraph("ANL-02-Model")

    # Remove comentários
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # Handle imports (just strip them for now)
    code = re.sub(r'import\s+[\w\.\*]+;', '', code)

    # 1. Namespaces
    ns_pattern = re.compile(r'namespace\s+(\w+)\s*\{')
    while True:
        match = ns_pattern.search(code)
        if not match: break

        ns_name = match.group(1)
        ns_body, next_pos = extract_nested_block(code, match.end())

        if ns_body:
            hg.namespaces[ns_name] = []
            inner_hg = compile_anl_v02(ns_body)
            for node_id, node in inner_hg.nodes.items():
                full_id = f"{ns_name}.{node_id}"
                node.id = full_id
                hg.add_node(node)
                hg.namespaces[ns_name].append(full_id)
            for h_id, h in inner_hg.handovers.items():
                h.id = f"{ns_name}.{h_id}"
                hg.add_handover(h)
            for e_name, e_vals in inner_hg.enums.items():
                hg.enums[f"{ns_name}.{e_name}"] = e_vals
            for d_name, d_body in inner_hg.dynamics.items():
                hg.dynamics[f"{ns_name}.{d_name}"] = d_body
            for c_id, c in inner_hg.constraints.items():
                c.id = f"{ns_name}.{c_id}"
                hg.add_constraint(c)

        code = code[:match.start()] + code[next_pos:]

    # 2. Enums
    enum_pattern = re.compile(r'enum\s+(\w+)\s*\{')
    while True:
        match = enum_pattern.search(code)
        if not match: break

        enum_name = match.group(1)
        enum_body, next_pos = extract_nested_block(code, match.end())

        if enum_body:
            enum_values = {}
            for line in split_by_top_level_semicolon(enum_body):
                if not line: continue
                m = re.match(r'(\w+)\s*(\{.*\})?', line, re.DOTALL)
                if m:
                    val_name = m.group(1)
                    val_content = m.group(2).strip() if m.group(2) else None
                    enum_values[val_name] = val_content
            hg.enums[enum_name] = enum_values

        code = code[:match.start()] + code[next_pos:]

    # 3. Global Dynamics
    dyn_pattern = re.compile(r'dynamic\s+(\w+)\s*\{')
    while True:
        match = dyn_pattern.search(code)
        if not match: break

        dyn_name = match.group(1)
        dyn_body, next_pos = extract_nested_block(code, match.end())

        if dyn_body:
            hg.dynamics[dyn_name] = dyn_body.strip()

        code = code[:match.start()] + code[next_pos:]

    # 4. Nós
    node_pattern = re.compile(r'node\s+(\w+)(?:\s*:\s*(\w+))?\s*\{')
    while True:
        match = node_pattern.search(code)
        if not match: break

        node_id = match.group(1)
        parent_id = match.group(2)
        body, next_pos = extract_nested_block(code, match.end())

        if body:
            attr_dict = {}
            attr_match = re.search(r'attributes\s*\{', body)
            if attr_match:
                attr_body, _ = extract_nested_block(body, attr_match.end())
                if attr_body:
                    for line in split_by_top_level_semicolon(attr_body):
                        if not line: continue
                        if '=' in line:
                            decl, val = line.split('=', 1)
                            decl_clean = re.sub(r'\[.*?\]', '', decl)
                            decl_parts = decl_clean.strip().split()
                            if len(decl_parts) >= 2:
                                attr_name = decl_parts[1]
                                attr_val = val.strip()
                                try:
                                    attr_dict[attr_name] = ast.literal_eval(attr_val)
                                except:
                                    attr_dict[attr_name] = attr_val
                        else:
                            decl_clean = re.sub(r'\[.*?\]', '', line)
                            decl_parts = decl_clean.strip().split()
                            if len(decl_parts) >= 2:
                                attr_name = decl_parts[1]
                                attr_dict[attr_name] = None

            dynamics_str = None
            dynamics_match = re.search(r'dynamics\s*\{', body)
            if dynamics_match:
                dynamics_body, _ = extract_nested_block(body, dynamics_match.end())
                dynamics_str = dynamics_body.strip() if dynamics_body else None

            # Capture functions
            functions = {}
            func_pattern = re.compile(r'function\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([\w<>]+))?\s*\{')
            func_pos = 0
            while True:
                f_match = func_pattern.search(body, func_pos)
                if not f_match: break
                f_name = f_match.group(1)
                f_body, f_next_pos = extract_nested_block(body, f_match.end())
                if f_body:
                    functions[f_name] = f_body.strip()
                func_pos = f_next_pos

            node = Node(node_id, StateSpace.euclidean(0), attributes=attr_dict, internal_dynamics=dynamics_str, parent_id=parent_id, functions=functions)
            hg.add_node(node)

        code = code[:match.start()] + code[next_pos:]

    # 5. Constraints
    const_pattern = re.compile(r'constraint\s+(\w+)\s*\{')
    while True:
        match = const_pattern.search(code)
        if not match: break

        c_id = match.group(1)
        body, next_pos = extract_nested_block(code, match.end())

        if body:
            mode = "runtime"
            mode_match = re.search(r'mode\s*:\s*(\w+);', body)
            if mode_match:
                mode = mode_match.group(1)

            measurement = None
            meas_match = re.search(r'measurement\s*\{', body)
            if meas_match:
                meas_body, _ = extract_nested_block(body, meas_match.end())
                measurement = meas_body.strip() if meas_body else None

            check = None
            check_match = re.search(r'check\s*:\s*([^;]+);', body)
            if not check_match:
                check_match_block = re.search(r'check\s*\{', body)
                if check_match_block:
                    check_body, _ = extract_nested_block(body, check_match_block.end())
                    check = check_body.strip()
            else:
                check = check_match.group(1).strip()

            on_violation = None
            viol_match = re.search(r'on_violation\s*:\s*(\w+)', body)
            if not viol_match:
                viol_match_block = re.search(r'on_violation\s*:\s*(\w+)\s*\{', body)
                if viol_match_block:
                    on_violation = viol_match_block.group(1)
            else:
                on_violation = viol_match.group(1)

            c = Constraint(c_id, check, mode=mode, measurement=measurement, on_violation=on_violation)
            hg.add_constraint(c)

        code = code[:match.start()] + code[next_pos:]

    # 6. Handovers
    handover_pattern = re.compile(r'handover\s+(\w+)\s*\(([^)]+)\)\s*\{')
    while True:
        match = handover_pattern.search(code)
        if not match: break

        h_id = match.group(1)
        params = match.group(2)
        body, next_pos = extract_nested_block(code, match.end())

        param_types = [p.strip().split()[0] for p in params.split(',')]

        if len(param_types) >= 2:
            src_name, dst_name = param_types[0], param_types[1]
            src = hg.nodes.get(src_name)
            if not src: src = Node(src_name, StateSpace.euclidean(0))
            dst = hg.nodes.get(dst_name)
            if not dst: dst = Node(dst_name, StateSpace.euclidean(0))

            condition = None
            cond_match = re.search(r'condition\s*:\s*([^;]+);', body)
            if cond_match:
                condition = cond_match.group(1).strip()

            effects = None
            effects_match = re.search(r'effects\s*\{', body)
            if effects_match:
                effects_body, _ = extract_nested_block(body, effects_match.end())
                effects = effects_body.strip() if effects_body else None

            protocol = Protocol.CREATIVE
            proto_match = re.search(r'protocol\s*:\s*(\w+);', body)
            if proto_match:
                try: protocol = Protocol[proto_match.group(1).upper()]
                except: pass

            h = Handover(h_id, src, dst, protocol, condition=condition, effects=effects)
            hg.add_handover(h)

        code = code[:match.start()] + code[next_pos:]

    return hg

def compile_anl_file(filename: str) -> dict:
    """
    Compila um arquivo .arkhe ou .anl em Arkhe Intermediate Representation (AIR).
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Arquivo {filename} não encontrado.")

    with open(filename, "r") as f:
        code = f.read()

    if re.search(r'(node|handover|namespace|enum|dynamic|constraint)\s+\w+', code):
        hg = compile_anl_v02(code)
    else:
        namespace = {
            'Hypergraph': Hypergraph, 'Node': Node, 'Handover': Handover,
            'StateSpace': StateSpace, 'Protocol': Protocol, 'Constraint': Constraint,
            'np': np,
        }
        try: exec(code, namespace)
        except Exception as e: raise RuntimeError(f"Erro ao executar o código ANL (Python DSL): {e}")
        hg = namespace.get('hypergraph')
        if hg is None:
            for val in namespace.values():
                if isinstance(val, Hypergraph): hg = val; break

    if hg is None: raise ValueError("Arquivo ANL deve definir uma instância de 'Hypergraph' ou conter definições de 'node'")
    return hg_to_air(hg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 anl_compiler.py <arquivo.anl|arquivo.arkhe>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = re.sub(r'\.(anl|arkhe)$', '.air.json', input_file)
    if output_file == input_file: output_file += ".air.json"
    try:
        air = compile_anl_file(input_file)
        with open(output_file, "w") as f:
            json.dump(air, f, indent=2)
            f.write("\n")
        print(f"✅ Compilação concluída: {output_file}")
    except Exception as e:
        print(f"❌ Erro na compilação: {e}")
        sys.exit(1)
