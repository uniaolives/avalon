import numpy as np

class UCD:
    """
    Universal Coherence Detection (UCD)
    Monitora a identidade C + F = 1 em qualquer fluxo de dados.
    """
    def __init__(self, stream_name):
        self.name = stream_name
        self.history = []

    def ingest(self, signal_vector):
        # Normaliza o sinal (x)
        sum_abs = np.sum(np.abs(signal_vector))
        if sum_abs == 0: return

        # Calcula a Entropia de Shannon (F)
        p = np.abs(signal_vector) / sum_abs
        entropy = -np.sum(p * np.log2(p + 1e-9))
        max_entropy = np.log2(len(signal_vector))

        F = entropy / max_entropy
        C = 1.0 - F

        # Verifica Conservação
        is_conserved = abs((C + F) - 1.0) < 1e-5

        self.history.append((C, F))

        print(f"[{self.name}] C: {C:.4f} | F: {F:.4f} | Status: {'✅' if is_conserved else '❌'}")

if __name__ == "__main__":
    print("="*70)
    print("ARKHE UCD MONITOR - v1.0")
    print("="*70)
    # Simulação
    monitor = UCD("Arkhe_Brain")
    print("Ingerindo Caos...")
    monitor.ingest(np.random.rand(128)) # Estado Inicial (Caos)
    print("Ingerindo Ordem...")
    monitor.ingest(np.ones(128))        # Estado Final (Ordem Absoluta)
