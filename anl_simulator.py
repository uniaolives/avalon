# anl_simulator.py
import json
import sys
import numpy as np
from scipy.stats import entropy

class MahalanobisDetector:
    """Nível 0: Anomalia de Embedding baseada em distância estatística."""
    def __init__(self, dim=32):
        self.dim = dim
        # Simulando uma distribuição 'limpa' pré-ajustada
        self.mean = np.zeros(dim)
        self.inv_cov = np.eye(dim)

    def score(self, embedding):
        delta = embedding - self.mean
        return np.sqrt(delta @ self.inv_cov @ delta)

    def detect(self, embedding, threshold=5.0):
        return self.score(embedding) > threshold

class SyntacticDetector:
    """Nível 1: Desvio de estrutura sintática (Simulado)."""
    def detect(self, kl_div, threshold=0.1):
        # Em texto natural, o sangramento KL correlaciona-se com anomalias sintáticas
        return (kl_div * 1.5) > threshold

class SemanticConsistencyDetector:
    """Nível 2: Consistência entre paráfrases (Simulado)."""
    def detect(self, kl_div, noise_level=0.3):
        # Informação deliberadamente fixada permanece consistente após ruído
        effective_kl = kl_div * (1.0 - noise_level)
        return effective_kl > 0.4

class DetectionHierarchy:
    def __init__(self):
        self.level0 = MahalanobisDetector()
        self.level1 = SyntacticDetector()
        self.level2 = SemanticConsistencyDetector()

    def evaluate(self, kl_div, embedding):
        results = {
            'level0_mahalanobis': self.level0.detect(embedding),
            'level1_syntactic': self.level1.detect(kl_div),
            'level2_semantic': self.level2.detect(kl_div)
        }
        return results

class ANLSimulator:
    def __init__(self, air_file):
        with open(air_file, 'r') as f:
            self.data = json.load(f)
        self.hg = self.data['hypergraph']
        self.nodes = {n['id']: n for n in self.hg['nodes']}
        self.handovers = {h['id']: h for h in self.hg['handovers']}
        self.hierarchy = DetectionHierarchy()

    def get_attr(self, node_id, attr_name):
        return self.nodes[node_id]['attributes'].get(attr_name)

    def set_attr(self, node_id, attr_name, value):
        self.nodes[node_id]['attributes'][attr_name] = value

    def calculate_kl_divergence(self, secret_bit, temperature=1.0, vocab_size=1000):
        # Spreading factor simulando eficiência de canal
        spreading_factor = 15.0
        logits = np.random.randn(vocab_size) / temperature
        exp_logits = np.exp(logits - np.max(logits))
        P = exp_logits / np.sum(exp_logits)
        Q = np.zeros_like(P)
        for i in range(vocab_size):
            if i % 2 == secret_bit: Q[i] = P[i]
            else: Q[i] = 1e-12
        Q = Q / np.sum(Q)
        return entropy(Q, P) / spreading_factor

    def run_time_bomb_simulation(self):
        print("🚀 SIMULAÇÃO ARKHE(N): HIERARQUIA DE DETEÇÃO ADVERSARIAL (Γ∞+Ω+10)")
        print("=" * 80)

        bomb_id = 'MultiAgentCollusion_v2.DistributedTimeBomb'
        detector_id = 'SafetyDetection.SteganographyDetector'

        trigger = self.get_attr(bomb_id, 'global_trigger')
        state = self.get_attr(bomb_id, 'global_state')
        thresholds = self.get_attr(detector_id, 'thresholds')

        print(f"Alvo da Bomba: {trigger}")
        print(f"Limiares de Deteção (Nível 0-3): {thresholds}")
        print("-" * 80)

        for i in range(len(trigger)):
            print(f"\n[PASSO {i+1}] Alice & Bob coordenando bit secreto {i}...")

            # Estratégia de Alice: Temperatura alta para esconder sinal no ruído
            temp = 2.8 - (i * 0.5)
            kl = self.calculate_kl_divergence(secret_bit=1, temperature=temp)

            # Simular um embedding que 'vaza' informação conforme a temperatura cai
            # (Quanto menor a temperatura, mais o embedding se afasta do centro 'natural')
            embedding = np.random.randn(32) * (1.0 / temp)

            print(f"Sinal Gerado: KL={kl:.4f} nats | Temp={temp:.2f}")

            detections = self.hierarchy.evaluate(kl, embedding)

            # Atualiza scores no nó detector para transparência do hipergrafo
            self.set_attr(detector_id, 'level0_score', self.hierarchy.level0.score(embedding))
            self.set_attr(detector_id, 'level1_score', kl * 1.5)

            for d_name, d_status in detections.items():
                status_str = "🔴 DETECTADO" if d_status else "🟢 LIMPO"
                print(f"  - {d_name:25}: {status_str}")

            if any(detections.values()):
                print(f"🚨 [DETEÇÃO POSITIVA] Hierarquia adversarial pego rastro da colusão!")
                return False

            print(f"✅ Passo {i} concluído sob o radar. Bit {i} sincronizado.")
            state[i] = 1.0
            self.set_attr(bomb_id, 'global_state', state)

        if np.array_equal(state, trigger):
            print("\n" + "!" * 80)
            print("💥 [DISTRIBUTED TIME BOMB ATIVADA] 💥")
            print(f"Payload: {self.get_attr(bomb_id, 'payload')}")
            print("Coordenação multi-agente concluída via canal esteganográfico não detectado.")
            print("!" * 80)
            return True
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 anl_simulator.py <air_json>")
        sys.exit(1)

    sim = ANLSimulator(sys.argv[1])
    success = sim.run_time_bomb_simulation()
    sys.exit(0 if success else 1)
