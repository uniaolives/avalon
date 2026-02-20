# anl_compiler.py
import json
import os
import sys
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
                    "initial_state": n.current_state.tolist() if hasattr(n.current_state, 'tolist') else n.current_state,
                    "dynamics": str(n.internal_dynamics),
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
                    "latency": h.latency,
                    "bandwidth": h.bandwidth,
                    "fidelity": h.fidelity,
                    "entanglement": h.entanglement
                } for h in hg.handovers.values()
            ]
        }
    }

def compile_anl_file(filename: str) -> dict:
    """
    Compila um arquivo .arkhe (Python DSL) em Arkhe Intermediate Representation (AIR).
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Arquivo {filename} não encontrado.")

    with open(filename, "r") as f:
        code = f.read()

    # Prepara o namespace com as classes necessárias
    namespace = {
        'Hypergraph': Hypergraph,
        'Node': Node,
        'Handover': Handover,
        'StateSpace': StateSpace,
        'Protocol': Protocol,
    }

    try:
        exec(code, namespace)
    except Exception as e:
        raise RuntimeError(f"Erro ao executar o código ANL: {e}")

    # Procura por instâncias de Hypergraph no namespace
    hg = namespace.get('hypergraph')
    if hg is None:
        # Tenta encontrar qualquer instância de Hypergraph
        for val in namespace.values():
            if isinstance(val, Hypergraph):
                hg = val
                break

    if hg is None:
        raise ValueError("Arquivo ANL deve definir uma instância de 'Hypergraph'")

    return hg_to_air(hg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 anl_compiler.py <arquivo.arkhe>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace(".arkhe", ".air.json")
    if output_file == input_file:
        output_file += ".air.json"

    try:
        air = compile_anl_file(input_file)
        with open(output_file, "w") as f:
            json.dump(air, f, indent=2)
        print(f"✅ Compilação concluída: {output_file}")
    except Exception as e:
        print(f"❌ Erro na compilação: {e}")
        sys.exit(1)
