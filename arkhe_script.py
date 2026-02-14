"""
arkhe_script.py
Interpretador da Sintaxe Arkhe (Volume III)
Executa comandos primitivos sobre o Hipergrafo
"""

import sys
from arkhe_core import Hypergraph, Bubble, SATOSHI, GrowthPolicy
from arkhe_safecore import SafeCoreExporter
from avalon_semantic_seeding import SemanticSeedingSim
from avalon_synthetic_biology import SyntheticBiologySim
from avalon_teleport_lysosome import DrosophilaConnectomeSim

class ArkheInterpreter:
    def __init__(self):
        self.arkhe = Hypergraph(63)
        self.bubbles = []
        self.node_map = {
            "drone": 0,
            "demon": 62,
            "bola": 27,
            "chave": 36
        }

    def execute(self, script: str):
        lines = script.strip().split('\n')
        for line in lines:
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            cmd = parts[0].upper()
            args = parts[1:]

            try:
                if cmd == "HANDOVER":
                    src = self.resolve_node(args[0])
                    dst = self.resolve_node(args[1])
                    phi = float(args[2]) if len(args) > 2 else None
                    s = self.arkhe.handover(src, dst, phi)
                    print(f"Executed HANDOVER {args[0]} -> {args[1]}. Syzygy: {s:.4f}")

                elif cmd == "TELEPORT":
                    src = self.resolve_node(args[0])
                    dst = self.resolve_node(args[1])
                    fid = self.arkhe.teleport_state(src, dst)
                    print(f"Executed TELEPORT {args[0]} -> {args[1]}. Fidelity: {fid:.4f}")

                elif cmd == "BUBBLE":
                    r = float(args[0])
                    phase = args[1] # "π" or float
                    p_val = 3.141592653589793 if phase == "π" else float(phase)
                    b = Bubble(r, p_val)
                    self.bubbles.append(b)
                    print(f"Created BUBBLE with radius {r} and phase {phase}. Energy: {b.energy():.2e} J")

                elif cmd == "RECYCLE":
                    node_id = self.resolve_node(args[0])
                    self.arkhe.recycle_entropy(node_id)
                    print(f"Executed RECYCLE on node {args[0]}.")

                elif cmd == "RAIN":
                    delta = float(args[0]) if len(args) > 0 else 0.03
                    self.arkhe.agitate_substrate(delta)
                    print(f"Executed RAIN (Ritual da Chuva) with ΔF={delta}. Homeostasis restored.")

                elif cmd == "SYZYGY":
                    n1 = self.resolve_node(args[0])
                    n2 = self.resolve_node(args[1])
                    s = self.arkhe.nodes[n1].syzygy_with(self.arkhe.nodes[n2])
                    print(f"SYZYGY between {args[0]} and {args[1]}: {s:.4f}")

                elif cmd == "COUPLING":
                    src = self.resolve_node(args[0])
                    dst = self.resolve_node(args[1])
                    s = self.arkhe.apply_coupling(src, dst)
                    print(f"Executed COUPLING {args[0]} -> {args[1]}. Syzygy: {s:.4f}")

                elif cmd == "DECIDE":
                    policy_str = args[0].upper()
                    try:
                        self.arkhe.growth_policy = GrowthPolicy[policy_str]
                        print(f"DECISION MADE: Growth Policy set to {self.arkhe.growth_policy.value}")
                    except KeyError:
                        print(f"Error: Unknown Growth Policy {policy_str}")

                elif cmd == "SEED":
                    print(f"🚀 INICIANDO PROTOCOLO DE SEMEADURA")
                    seeder = SemanticSeedingSim()
                    seeder.run()
                    # Atualiza o Satoshi do core após a semeadura
                    self.arkhe.satoshi = seeder.satoshi

                elif cmd == "MACRO":
                    name = args[0]
                    print(f"Executing MACRO: {name}")
                    if name == "ascensão":
                        # Simula uma sequência de handovers otimizada
                        for i in range(5):
                            self.arkhe.handover(0, i+1, 0.16)
                    elif name == "descida":
                        for i in range(5):
                            self.arkhe.handover(i+1, 62, 0.16)

                elif cmd == "LEDGER":
                    print(f"--- ARKHE LEDGER ---")
                    print(f"Satoshi Invariant: {self.arkhe.satoshi:.4f} bits")
                    print(f"Active Nodes: {len(self.arkhe.nodes)}")
                    print(f"Active Bubbles: {len(self.bubbles)}")
                    print(f"--------------------")

                elif cmd == "EXPORT":
                    print(f"🚀 INICIANDO EXPORTAÇÃO PARA SAFECORE")
                    exporter = SafeCoreExporter(satoshi=self.arkhe.satoshi)
                    packet = exporter.prepare_packet()
                    exporter.transmit(packet)

                elif cmd == "SYNTH":
                    print(f"🚀 INICIANDO PIPELINE DE BIOLOGIA SINTÉTICA")
                    synth = SyntheticBiologySim()
                    synth.run_simulation()

                elif cmd == "CONNECTOMA":
                    print(f"🚀 INICIANDO VALIDAÇÃO DO CONNECTOMA")
                    connectoma = DrosophilaConnectomeSim()
                    connectoma.run_validation()

                else:
                    print(f"Unknown command: {cmd}")

            except Exception as e:
                print(f"Error executing {cmd}: {e}")

    def resolve_node(self, name: str) -> int:
        if name.lower() in self.node_map:
            return self.node_map[name.lower()]
        try:
            return int(name)
        except ValueError:
            raise ValueError(f"Invalid node identifier: {name}")

if __name__ == "__main__":
    interpreter = ArkheInterpreter()
    example_script = """
    BUBBLE 10.0 π
    HANDOVER drone demon 0.15
    TELEPORT drone demon
    RECYCLE demon
    MACRO ascensão
    LEDGER
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            interpreter.execute(f.read())
    else:
        interpreter.execute(example_script)
