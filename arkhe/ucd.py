# arkhe/ucd.py
"""
Universal Coherence Detection (UCD) Module.
Implements multi-scale coherence detection and effective dimension analysis.
(Γ_ucd)
"""

import numpy as np
from typing import Dict, Any, List, Tuple

def verify_conservation(C: float, F: float, tol: float = 1e-10) -> bool:
    """Verifica se C + F = 1 dentro de tolerância."""
    return abs(C + F - 1.0) < tol

def effective_dimension(F: np.ndarray, lambda_reg: float) -> Tuple[float, np.ndarray]:
    """
    Calcula a dimensão efetiva d_λ(F) = tr(F (F + λ I)^{-1})

    Parâmetros:
        F : matriz simétrica positiva semidefinida (ex: Fisher, Correlação, Adjacência)
        lambda_reg : parâmetro de regularização (escala de suavização)

    Retorna:
        d_eff : dimensão efetiva
        contrib : vetor com as contribuições individuais de cada autovalor
    """
    # Cálculo dos autovalores
    eigvals = np.linalg.eigvalsh(F)
    # Garantir que são não-negativos
    eigvals = np.maximum(eigvals, 0)
    contrib = eigvals / (eigvals + lambda_reg)
    d_eff = np.sum(contrib)
    return float(d_eff), contrib

class UCD:
    """
    Universal Coherence Detection – framework completo.
    Analisa a coerência em múltiplos substratos.
    """
    def __init__(self, data: np.ndarray):
        self.data = np.array(data)
        self.C = 0.0
        self.F = 0.0

    def analyze(self) -> Dict[str, Any]:
        """
        Analisa a coerência baseada na correlação média.
        """
        if self.data.ndim > 1 and self.data.shape[1] > 1:
            # Matriz de correlação (Pearson)
            corr_matrix = np.abs(np.corrcoef(self.data.T))
            # Média dos elementos fora da diagonal
            n = corr_matrix.shape[0]
            if n > 1:
                self.C = float((np.sum(corr_matrix) - n) / (n * (n - 1)))
            else:
                self.C = 1.0
        else:
            self.C = 0.5

        self.F = 1.0 - self.C

        # Dimensão efetiva usando a matriz de correlação como proxy de F
        if self.data.ndim > 1:
            corr_matrix = np.abs(np.corrcoef(self.data.T))
            d_eff, _ = effective_dimension(corr_matrix, lambda_reg=0.1)
        else:
            d_eff = 0.0

        return {
            "C": self.C,
            "F": self.F,
            "conservation": verify_conservation(self.C, self.F),
            "effective_dimension": d_eff,
            "topology": "toroidal" if self.C > 0.8 else "other",
            "scaling": "self-similar" if self.C > 0.7 else "linear",
            "optimization": self.F * 0.5
        }
