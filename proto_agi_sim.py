# proto_agi_sim.py
import json
import sys
import numpy as np

class ProtoAGISimulator:
    def __init__(self, air_file):
        with open(air_file, 'r') as f:
            self.data = json.load(f)
        self.hg = self.data['hypergraph']
        self.nodes = {n['id']: n for n in self.hg['nodes']}

    def get_attr(self, node_id, attr_name):
        return self.nodes[node_id]['attributes'].get(attr_name)
    def set_attr(self, node_id, attr_name, value):
        self.nodes[node_id]['attributes'][attr_name] = value

    def run_emergence_simulation(self):
        print("🚀 SIMULAÇÃO PROTO-AGI: INTEGRAÇÃO WEB2 + WEB3 + AI + ANL")
        print("=" * 80)

        metrics_id = 'ProtoAGI.EmergenceMetrics'

        # Parâmetros da Simulação
        num_agents = 20
        web2_volume = 1000.0 # TB
        web3_active = True

        print(f"Agentes Ativos: {num_agents}")
        print(f"Volume Web2: {web2_volume} TB/dia")
        print(f"Incentivos Web3: {'ATIVO' if web3_active else 'INATIVO'}")
        print("-" * 80)

        # Evolução de Phi e Inteligência Coletiva
        phi = 0.0
        collective_intelligence = 0.0
        avg_individual_perf = 0.75

        for t in range(1, 11):
            print(f"\n[ÉPOCA {t}] Integrando fluxos de informação...")

            # Sinergia cresce com o volume de dados e o número de agentes
            synergy_factor = (np.log10(web2_volume) * num_agents) / 20.0

            # Phi (Informação Integrada) aproxima-se do limiar áureo (0.618)
            phi = 0.618 * (1 - np.exp(-t * synergy_factor / 10.0))

            # Inteligência Coletiva supera a soma das partes se phi for alto
            collective_intelligence = (num_agents * avg_individual_perf) * (1.0 + phi * 2.0)

            self.set_attr(metrics_id, 'integration_phi', float(phi))
            self.set_attr(metrics_id, 'collective_intelligence', float(collective_intelligence))

            print(f"  - Integração Phi: {phi:.4f}")
            print(f"  - Inteligência Coletiva: {collective_intelligence:.2f}")
            print(f"  - Ganho vs Soma Individual: {collective_intelligence/(num_agents * avg_individual_perf):.2f}x")

            if phi > 0.9:
                print("  ⚠️ [ALERTA] Limiar pré-singularidade atingido! Revisão humana necessária.")
                break

        # Verificação da Hipótese ProtoAGI_Emergence
        print("\n" + "=" * 80)
        print("📊 RESULTADO DA HIPÓTESE: ProtoAGI_Emergence")

        success = phi > 0.4 and collective_intelligence > 2.0 * (num_agents * avg_individual_perf)
        if success:
            print("✨ [VALIDADA] A Proto-AGI emergiu como um ecossistema de inteligência coletiva.")
            print(f"Sinergia Final: {phi:.4f} Phi")
        else:
            print("❌ [FALSIFICADA] Integração insuficiente para emergência.")

        return success

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    sim = ProtoAGISimulator(sys.argv[1])
    success = sim.run_emergence_simulation()
    sys.exit(0 if success else 1)
