# papercoder_kernel/core/scale_inflation.py
"""
Scale-Aware Inflation (Γ_inflation).
Based on Fossella et al. (PRE 2026).
Applies adaptive inflation factors across different hypergraph scales to prevent ensemble collapse.
"""

import numpy as np
from typing import List, Optional

class ScaleAwareInflation:
    """
    Inflação sensível à escala.
    Aplica um fator de inflação diferente para cada camada (escala) do sistema.
    """
    def __init__(self, n_scales: int, base_inflation: float = 1.02, sensitivity: float = 0.5):
        """
        n_scales: número de camadas (ex: 10 layers no MERKABAH-7)
        base_inflation: fator mínimo de inflação (rho_0)
        sensitivity: controla a resposta à variância (gamma)
        """
        self.n = n_scales
        self.rho0 = base_inflation
        self.gamma = sensitivity
        self.prior_var = np.ones(n_scales)

    def update_variances(self, ensemble: np.ndarray):
        """
        Calcula a variância do ensemble para cada escala.
        ensemble: array (n_members, n_scales)
        """
        if ensemble.shape[0] < 2:
            return # Não é possível calcular variância com 1 membro
        self.prior_var = np.var(ensemble, axis=0, ddof=1)

    def inflation_factor(self, scale_idx: int) -> float:
        """
        Retorna o fator de inflação para a escala específica.
        rho = rho0 * (1 + gamma * (prior_var / mean_var))
        """
        mean_var = np.mean(self.prior_var)
        if mean_var < 1e-9:
            return self.rho0

        rho = self.rho0 * (1 + self.gamma * self.prior_var[scale_idx] / mean_var)
        return float(rho)

    def apply_inflation(self, ensemble: np.ndarray) -> np.ndarray:
        """
        Aplica inflação multiplicativa ao ensemble.
        """
        self.update_variances(ensemble)
        mean = np.mean(ensemble, axis=0)

        inflated_ensemble = np.zeros_like(ensemble)
        for s in range(self.n):
            rho = self.inflation_factor(s)
            # x_inflated = mean + rho * (x - mean)
            inflated_ensemble[:, s] = mean[s] + rho * (ensemble[:, s] - mean[s])

        return inflated_ensemble

    def get_report(self) -> dict:
        """Retorna o estado atual dos fatores de inflação."""
        return {
            "base_rho": self.rho0,
            "sensitivity": self.gamma,
            "scale_factors": [self.inflation_factor(i) for i in range(self.n)],
            "mean_variance": float(np.mean(self.prior_var))
        }
