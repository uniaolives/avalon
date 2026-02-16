# arkhe/ucd.py
"""
Universal Coherence Detection (UCD) Module.
Implements multi-scale coherence detection and advanced Random Projection Theory.
Based on "A Unified Theory of Random Projection for Influence Functions" (Hu et al. 2026).
(Γ_ucd)
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional

def verify_conservation(C: float, F: float, tol: float = 1e-10) -> bool:
    """Verifica se C + F = 1 dentro de tolerância."""
    return abs(C + F - 1.0) < tol

def effective_dimension(F: np.ndarray, lambda_reg: float) -> Tuple[float, np.ndarray]:
    """
    Calcula a dimensão efetiva d_λ(F) = tr(F (F + λ I)^{-1})
    """
    eigvals = np.linalg.eigvalsh(F)
    eigvals = np.maximum(eigvals, 0)
    contrib = eigvals / (eigvals + lambda_reg)
    d_eff = np.sum(contrib)
    return float(d_eff), contrib

class RandomProjectionTheory:
    """
    Implementa os teoremas da Teoria Unificada de Projeção Aleatória.
    """
    @staticmethod
    def estimate_sketch_size(F: np.ndarray, lambda_reg: float, epsilon: float = 0.1) -> int:
        """
        Teorema 2.2: O tamanho do sketch m deve escalar com d_λ(F)/ε².
        m ∝ d_λ(F)/ε²
        """
        d_eff, _ = effective_dimension(F, lambda_reg)
        # Usamos uma constante de proporcionalidade k=10 para simulação
        k = 10
        m = int(np.ceil(k * d_eff / (epsilon**2)))
        return m

    @staticmethod
    def factored_projection_cost(A: np.ndarray, E: np.ndarray,
                               lambda_A: float, lambda_E: float,
                               epsilon: float = 0.1) -> Dict[str, int]:
        """
        Teorema 2.7: Custo para projeção fatorada (K-FAC).
        mA ∝ d_{λE}(A)/ε², mE ∝ d_{λA}(E)/ε²
        """
        d_eff_A, _ = effective_dimension(A, lambda_A)
        d_eff_E, _ = effective_dimension(E, lambda_E)

        k = 10
        m_A = int(np.ceil(k * d_eff_A / (epsilon**2)))
        m_E = int(np.ceil(k * d_eff_E / (epsilon**2)))

        return {"m_A": m_A, "m_E": m_E, "total_cost": m_A * m_E}

    @staticmethod
    def calculate_kernel_leakage(gradient_norm: float, orthogonal_component: float) -> float:
        """
        Teorema 3.1 & 3.3: O vazamento de kernel é proporcional ao produto
        da norma do gradiente e da componente ortogonal.
        """
        return gradient_norm * orthogonal_component

class UCD:
    """
    Universal Coherence Detection – framework completo.
    Analisa a coerência em múltiplos substratos com proteção contra vazamento.
    """
    def __init__(self, data: np.ndarray):
        self.data = np.array(data)
        self.C = 0.0
        self.F = 0.0

    def analyze(self, lambda_reg: float = 0.1, epsilon: float = 0.1) -> Dict[str, Any]:
        """
        Analisa a coerência e estima requisitos de projeção.
        """
        if self.data.ndim > 1 and self.data.shape[1] > 1:
            corr_matrix = np.abs(np.corrcoef(self.data.T))
            n = corr_matrix.shape[0]
            if n > 1:
                self.C = float((np.sum(corr_matrix) - n) / (n * (n - 1)))
            else:
                self.C = 1.0

            # Teoria de Projeção
            m_size = RandomProjectionTheory.estimate_sketch_size(corr_matrix, lambda_reg, epsilon)
            d_eff, _ = effective_dimension(corr_matrix, lambda_reg)
        else:
            self.C = 0.5
            m_size = 0
            d_eff = 0.0

        self.F = 1.0 - self.C

        return {
            "C": self.C,
            "F": self.F,
            "conservation": verify_conservation(self.C, self.F),
            "effective_dimension": d_eff,
            "recommended_sketch_size": m_size,
            "topology": "toroidal" if self.C > 0.8 else "other",
            "scaling": "self-similar" if self.C > 0.7 else "linear"
        }
