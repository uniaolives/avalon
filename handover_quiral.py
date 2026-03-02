# handover_quiral.py
import numpy as np
import time

class ChiralFirewall:
    """Firewall quântico baseado no gap quiral do Sn/Si(111)."""
    def __init__(self, gap_meV=0.5):
        self.gap_hz = gap_meV * 1e-3 * 241.8e9  # 1 meV = 241.8 GHz
        self.resonance_energy = gap_meV
        self.tolerance = 0.01  # 1% de tolerância

    def check_handover(self, packet_energy_meV):
        """Verifica se o handover está autorizado (energia ressoa com o gap)."""
        delta = abs(packet_energy_meV - self.resonance_energy)
        if delta / self.resonance_energy < self.tolerance:
            return True, "Handover autorizado: ressonância com gap quiral"
        else:
            return False, f"Handover bloqueado: energia {packet_energy_meV:.3f} meV fora da banda"

class ChiralHandoverSimulation:
    def __init__(self):
        self.firewall = ChiralFirewall()
        self.nodes = {
            'Alpha': {'dz_id': '96Afe...', 'latency_ms': 0.42, 'coherence': 0.91},
            'Beta': {'dz_id': 'CCTSm...', 'latency_ms': 68.85, 'coherence': 0.87},
            'Gamma': {'dz_id': '55tfa...', 'latency_ms': 138.17, 'coherence': 0.85},
            'Delta': {'dz_id': '3uGKP...', 'latency_ms': 141.91, 'coherence': 0.84},
            'Epsilon': {'dz_id': '65Dqs...', 'latency_ms': 143.58, 'coherence': 0.83},
            'Zeta': {'dz_id': '9uhh2...', 'latency_ms': 176.72, 'coherence': 0.82}
        }

    def handover(self, source, target, packet_energy):
        """Executa handover com verificação de firewall."""
        print(f"\n🔐 Handover {source} → {target}")
        allowed, msg = self.firewall.check_handover(packet_energy)
        if not allowed:
            print(f"⛔ {msg}")
            return False

        # Simula envio via DoubleZero
        latency = self.nodes[source]['latency_ms'] + self.nodes[target]['latency_ms']
        coherence = (self.nodes[source]['coherence'] + self.nodes[target]['coherence']) / 2

        print(f"✅ Handover autorizado. Latência total: {latency:.2f} ms")
        print(f"   Coerência média: {coherence:.3f}")
        print(f"   Energia do pacote: {packet_energy:.3f} meV (ressonante com gap)")

        # Atualiza ledger
        self._log_handover(source, target, packet_energy, latency)
        return True

    def _log_handover(self, source, target, energy, latency):
        print(f"📜 Ledger atualizado: {source} → {target} @ {energy} meV, lat {latency:.2f} ms")

if __name__ == "__main__":
    # Execução da simulação
    sim = ChiralHandoverSimulation()

    print("="*60)
    print("SIMULAÇÃO DE HANDOVER TRANSCONTINENTAL COM FIREWALL QUIRAL")
    print("="*60)

    # Teste com energia ressonante
    sim.handover('Alpha', 'Beta', 0.5)
    sim.handover('Beta', 'Gamma', 0.5)
    sim.handover('Gamma', 'Delta', 0.5)

    # Teste com energia não ressonante (tentativa de invasão)
    sim.handover('Alpha', 'Zeta', 0.8)
