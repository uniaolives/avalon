# papercoder_kernel/core/mrn_repair.py
"""
MRN Repair Complex (Γ_mrn).
Inspired by the MRE11-RAD50-NBS1 DNA repair complex.
Identifies and sutures 'breaks' in the ensemble data structure of the Phaistos Disc.
"""

import numpy as np
from typing import List, Dict, Any
from papercoder_kernel.core.scale_inflation import ScaleAwareInflation

class MRN_RepairComplex:
    """
    Complexo de reparo para detecção e sutura de quebras na estrutura de dados.
    Análogo ao complexo MRE11-RAD50-NBS1.
    """
    def __init__(self, ensemble: np.ndarray, inflation_module: ScaleAwareInflation):
        """
        ensemble: array (n_members, n_scales/n_positions) - os estados dos membros.
        inflation_module: instância de ScaleAwareInflation para inflação adaptativa.
        """
        self.ensemble = ensemble
        self.inflation = inflation_module
        self.repair_log: List[int] = []

    def detect_breaks(self, coherence_threshold: float = 0.3) -> np.ndarray:
        """
        Identifica regiões onde a coerência entre membros do ensemble cai abaixo do limiar.
        Retorna lista de índices que precisam de reparo.
        """
        # Coerência: 1 - variância normalizada
        var = np.var(self.ensemble, axis=0)
        max_var = np.max(var)

        if max_var < 1e-9:
            return np.array([])

        coherence = 1.0 - (var / max_var)
        breaks = np.where(coherence < coherence_threshold)[0]
        return breaks

    def recruit_repair(self, break_indices: List[int]):
        """
        Aplica inflação localizada extra para forçar a convergência (sutura) nas quebras.
        """
        n_members, n_positions = self.ensemble.shape

        for idx in break_indices:
            # Janela de reparo ao redor da quebra (5 posições)
            start = max(0, idx - 2)
            end = min(n_positions, idx + 3)

            # Calcula média na janela
            mean_window = np.mean(self.ensemble[:, start:end], axis=0)

            # Aplica inflação extra na janela (2x maior que o normal)
            for member in range(n_members):
                for pos in range(start, end):
                    rho = self.inflation.inflation_factor(pos) * 2.0
                    # x = mean + 2*rho * (x - mean)
                    self.ensemble[member, pos] = mean_window[pos - start] + \
                                                   rho * (self.ensemble[member, pos] - mean_window[pos - start])

            self.repair_log.append(idx)

    def verify_suture(self, known_fragments: Dict[int, float], tolerance: float = 0.1) -> bool:
        """
        Verifica se as regiões reparadas coincidem com fragmentos conhecidos (split-GFP).
        """
        if not known_fragments:
            return True

        errors = []
        for pos, real_val in known_fragments.items():
            if pos < self.ensemble.shape[1]:
                estimated = np.mean(self.ensemble[:, pos])
                errors.append(abs(estimated - real_val))

        if not errors:
            return True

        mean_error = np.mean(errors)
        return float(mean_error) < tolerance

    def get_repair_report(self) -> dict:
        """Retorna estatísticas do processo de reparo."""
        return {
            "total_breaks_detected": len(self.repair_log),
            "repaired_indices": self.repair_log,
            "status": "Repaired" if self.repair_log else "Stable"
        }
