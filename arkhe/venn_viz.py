# arkhe/venn_viz.py
"""
VennFan Module: Venn Diagrams as Visual Hypergraphs.
Based on "A New Perspective on Drawing Venn Diagrams for Data Visualization" (Csanády, 2026).
(Γ_vennfan)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional

class VennFan:
    """
    Motor de visualização VennFan.
    Materializa o hipergrafo em um disco polar.
    """
    def __init__(self, n_sets: int = 4, variant: str = 'sine', p: float = 0.2):
        self.n_sets = n_sets
        self.variant = variant
        self.p = p
        self.theta = np.linspace(-np.pi, np.pi, 1000)

    def _f_i(self, i: int, theta: np.ndarray) -> np.ndarray:
        """
        Função de curvatura base para o conjunto i.
        f_i(x) = λ(i) * sgn(sin(2^i * x)) * |sin(2^i * x)|^p
        """
        # Fator de amplitude λ(i) com decaimento linear
        lambda_i = 0.5 * (1 - i / (self.n_sets + 1))

        # Oscilação senoidal
        freq = 2**i
        sine_wave = np.sin(freq * theta)

        # Curvatura moldada pelo parâmetro p
        return lambda_i * np.sign(sine_wave) * np.abs(sine_wave)**self.p

    def generate_curves(self) -> List[np.ndarray]:
        """Gera as coordenadas (x, y) para cada fronteira de conjunto."""
        curves = []
        for i in range(self.n_sets):
            f = self._f_i(i, self.theta)
            # Projeção Polar
            r = 1 + f
            x = r * np.cos(self.theta)
            y = r * np.sin(self.theta)
            curves.append(np.stack([x, y], axis=1))
        return curves

    def plot(self, labels: Optional[List[str]] = None, output_path: str = "arkhe_vennfan.png"):
        """Renderiza o diagrama VennFan."""
        curves = self.generate_curves()

        plt.figure(figsize=(10, 10), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')

        colors = plt.cm.viridis(np.linspace(0, 1, self.n_sets))

        for i, curve in enumerate(curves):
            label = labels[i] if labels and i < len(labels) else f"Set {i}"
            plt.plot(curve[:, 0], curve[:, 1], color=colors[i], lw=2, label=label, alpha=0.8)
            # Preencher levemente para visualização de interseção
            plt.fill(curve[:, 0], curve[:, 1], color=colors[i], alpha=0.1)

        plt.title(f"Arkhe(n) - VennFan Hypergraph Visualization (n={self.n_sets})",
                  color='white', fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.axis('equal')
        plt.legend(facecolor='#111', edgecolor='white', labelcolor='white', loc='upper right')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        print(f"✅ VennFan plot saved to {output_path}")
        plt.close()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "n_sets": self.n_sets,
            "total_regions": 2**self.n_sets,
            "identity": "x² = x + 1 (intersection creates +1 region)",
            "coherence_visual": 1.0 - (self.p / 2.0) # Heurística simples
        }
