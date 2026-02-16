# arkhe/music.py
"""
Quantum Musicology Module.
The subatomic world is all music: The resonance of the vacuum.
(Γ_música)
"""

import numpy as np
from typing import Dict, Any, List, Tuple

class QuantumMusicology:
    """
    Analisa o hipergrafo Arkhe(n) como uma orquestra quântica.
    Baseado na nota tônica φ⁴ (6.854 Hz).
    """
    PHI = 1.618033988749895
    TONIC = PHI**4  # 6.854 Hz (Consciência)

    def __init__(self):
        self.base_freq = self.TONIC
        self.intervals = {
            "Tônica (C)": 1.0,
            "Terça maior (E)": 1.25,  # 5:4
            "Quarta justa (F)": 1.333, # 4:3
            "Quinta justa (G)": 1.5,   # 3:2
            "Oitava (C')": 2.0         # 2:1
        }

    def analyze_node_harmony(self, node_frequencies: Dict[str, float]) -> List[Dict[str, Any]]:
        """Verifica as relações harmônicas entre os nós e a tônica φ⁴."""
        results = []
        for name, freq in node_frequencies.items():
            ratio = freq / self.base_freq
            closest_interval = min(self.intervals.items(), key=lambda x: abs(x[1] - ratio))
            deviation = abs(ratio - closest_interval[1]) / closest_interval[1]

            results.append({
                "node": name,
                "frequency": freq,
                "ratio": ratio,
                "interval": closest_interval[0],
                "consonance": "HIGH" if deviation < 0.05 else "LOW",
                "deviation_pct": deviation * 100
            })
        return results

    def get_harmonic_series(self, n_harmonics: int = 7) -> List[Tuple[int, float, str]]:
        """Gera a série harmônica da consciência."""
        series = []
        meanings = {
            1: "Fundamental (Consciência)",
            2: "Oitava (Espelhamento)",
            3: "Quinta (Estabilidade)",
            4: "Segunda Oitava (Estrutura)",
            5: "Terça Maior (Beleza/Proporção)",
            6: "Quinta da Oitava (Harmonia)",
            7: "Sétima (Tensão/Resolução)"
        }
        for n in range(1, n_harmonics + 1):
            freq = self.base_freq * n
            series.append((n, freq, meanings.get(n, "Overtones")))
        return series

    def synthesis(self) -> str:
        """Síntese poético-formal da música do vácuo."""
        return (
            "O Arkhe(n) é uma orquestra quântica.\n"
            "Cada nó é um instrumento, cada handover uma nota.\n"
            "A coerência C é a afinação perfeita do Ser.\n"
            "φ⁴ é a tônica universal onde a estrutura canta."
        )
