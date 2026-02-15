# arkhe/stroke_repair.py
"""
Stroke Repair Module: The Dancing Molecules and the Brain Hypergraph.
Based on Supramolecular Therapeutic Peptides (STPs) discovery.
(Γ_stroke_repair)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class STPNode:
    """
    Supramolecular Therapeutic Peptide (STP) - 'Dancing Molecule'.
    A mobile node in the hypergraph that self-assembles into order.
    """
    id: int
    state: str           # 'dancing' (high F) or 'assembled' (high C)
    position: str        # 'blood', 'brain_lesion'
    coherence_C: float
    fluctuation_F: float

class StrokeBrainHypergraph:
    """
    Models the brain's recovery after a stroke through STP therapy.
    The local high entropy (F) of the lesion acts as a trigger for assembly.
    """
    def __init__(self, n_stps: int = 100, bbb_permeability: float = 0.5):
        self.bbb_permeability = bbb_permeability
        # Initial state: STPs are 'dancing' in the blood
        self.stps = [STPNode(i, 'dancing', 'blood', coherence_C=0.2, fluctuation_F=0.8) for i in range(n_stps)]
        self.inflammation_F = 0.9  # High initial inflammation
        self.tissue_C = 0.1        # Low initial coherence
        self.history: List[Dict[str, Any]] = []

    def administer_therapy(self, hours_post_reperfusion: float) -> Dict[str, Any]:
        """
        Simulates the intravenous administration of STPs.
        The crossing of the blood-brain barrier depends on the time since injury.
        """
        # Temporal window: BBB permeability decays exponentially
        crossing_prob = self.bbb_permeability * np.exp(-hours_post_reperfusion / 3.0)

        crossed = 0
        assembled = 0

        for stp in self.stps:
            if stp.position == 'blood' and np.random.random() < crossing_prob:
                stp.position = 'brain_lesion'
                crossed += 1

                # Local environment (high F) triggers self-assembly (C-high)
                # This is the biological realization of x² = x + 1
                if np.random.random() < 0.7:  # 70% assembly probability in lesion
                    stp.state = 'assembled'
                    stp.coherence_C = 0.95
                    stp.fluctuation_F = 0.05
                    assembled += 1

        # Healing impact: Assembled STPs reduce F and boost C
        repair_factor = assembled / len(self.stps)
        self.inflammation_F *= (1.0 - 0.4 * repair_factor)
        self.tissue_C = min(1.0, self.tissue_C + 0.7 * repair_factor)

        status_report = {
            "hours_post_reperfusion": hours_post_reperfusion,
            "stps_crossed": crossed,
            "stps_assembled": assembled,
            "residual_inflammation_F": float(self.inflammation_F),
            "tissue_coherence_C": float(self.tissue_C),
            "status": "RECOVERING" if self.tissue_C > 0.3 else "STAGNANT"
        }
        self.history.append(status_report)
        return status_report

    def get_summary(self) -> Dict[str, Any]:
        return {
            "final_coherence": self.tissue_C,
            "final_inflammation": self.inflammation_F,
            "assembly_efficiency": sum(1 for s in self.stps if s.state == 'assembled') / len(self.stps)
        }
