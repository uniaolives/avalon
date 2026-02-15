# arkhe/biomimesis.py
"""
Spider Silk Biomimesis: Molecular Hypergraph Architecture.
Now includes Universal Phase Control (Symmetry between Silk and Neural Repair).
(Γ_biomimesis)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any

@dataclass
class AminoAcidNode:
    """
    Node representing amino acid residue.
    Arginine (R): Cation (positive charge).
    Tyrosine (Y): Pi-cloud (aromatic ring).
    """
    node_id: str
    residue_type: str  # 'R' or 'Y'
    charge: float      # Potential for Arg
    pi_cloud: float    # Potential for Tyr
    coherence_C: float
    in_liquid_phase: bool = True

    def can_bond_with(self, other: 'AminoAcidNode') -> bool:
        """Cation-pi bond requires one cation (R) and one pi-cloud (Y)."""
        return (
            (self.residue_type == 'R' and other.residue_type == 'Y') or
            (self.residue_type == 'Y' and other.residue_type == 'R')
        )

    def bond_strength(self, other: 'AminoAcidNode') -> float:
        """Calculates cation-pi interaction strength."""
        if not self.can_bond_with(other):
            return 0.0
        strength = self.charge * other.pi_cloud if self.residue_type == 'R' else other.charge * self.pi_cloud
        return float(np.clip(strength, 0.0, 1.0))

class UniversalPhaseControl:
    """
    Equação Mestra que une a Seda (Força) e a Medula (Cura).
    Unifica a Transição de Fase Controlada no Hipergrafo.
    """
    @staticmethod
    def calculate_phase_efficiency(C_gain: float, F_loss: float) -> float:
        """
        Calcula a eficiência da transição: (ΔC / ΔF) * φ.
        Reflete o equilíbrio áureo entre ordem e flexibilidade.
        """
        phi = 1.618033988749895
        return float((C_gain / (F_loss + 1e-6)) * phi)

class SpiderSilkHypergraph:
    def __init__(self, n_nodes: int = 100):
        self.nodes: List[AminoAcidNode] = []
        self.bonds: List[Tuple[str, str, float]] = []
        for i in range(n_nodes):
            res_type = 'R' if i % 2 == 0 else 'Y'
            self.nodes.append(AminoAcidNode(
                node_id=f"Res_{i}", residue_type=res_type,
                charge=0.9 if res_type == 'R' else 0.0,
                pi_cloud=0.85 if res_type == 'Y' else 0.0,
                coherence_C=0.3
            ))
        self.global_C = 0.3
        self.global_F = 0.7

    def trigger_phase_separation(self, shear_force: float = 1.0) -> Dict[str, Any]:
        """Liquid -> Solid (C-high) for Strength."""
        pre_c = self.global_C
        pre_f = self.global_F

        new_bonds = 0
        for i, node_a in enumerate(self.nodes):
            if not node_a.in_liquid_phase: continue
            for node_b in self.nodes[i+1:]:
                if not node_b.in_liquid_phase: continue
                strength = node_a.bond_strength(node_b)
                if strength * shear_force > 0.65:
                    self.bonds.append((node_a.node_id, node_b.node_id, strength))
                    node_a.in_liquid_phase = node_b.in_liquid_phase = False
                    node_a.coherence_C = node_b.coherence_C = 0.95
                    new_bonds += 1

        solid_count = sum(1 for n in self.nodes if not n.in_liquid_phase)
        self.global_C = 0.3 + 0.7 * (solid_count / len(self.nodes))
        self.global_F = 1.0 - self.global_C

        # Aplicar Equação Mestra
        efficiency = UniversalPhaseControl.calculate_phase_efficiency(
            self.global_C - pre_c, pre_f - self.global_F
        )

        return {
            "phase": "SOLID_FIBER" if self.global_C > 0.8 else "TRANSITIONING",
            "coherence": self.global_C,
            "fluctuation": self.global_F,
            "efficiency": efficiency,
            "bonds": len(self.bonds)
        }

class AlzheimerProteinAggregation:
    """Contrast: Uncontrolled aggregation (F-high)."""
    def __init__(self, n_nodes: int = 100):
        self.nodes = [{"id": i, "state": "HEALTHY", "C": 0.8} for i in range(n_nodes)]
        self.global_C = 0.8

    def simulate_stress(self, entropy_level: float = 0.5) -> Dict[str, Any]:
        print(f"🧠 [ALZHEIMER] Estresse: {entropy_level:.2f}")
        aggregated = 0
        for n in self.nodes:
            if n["state"] == "HEALTHY" and np.random.random() < entropy_level:
                n["state"] = "AGGREGATED"
                n["C"] = 0.1
                aggregated += 1
        self.global_C = np.mean([n["C"] for n in self.nodes])
        return {
            "status": "CRITICAL" if self.global_C < 0.4 else "STABLE",
            "coherence": float(self.global_C),
            "aggregated_ratio": aggregated / len(self.nodes)
        }
