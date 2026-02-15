# arkhe/biomimesis.py
"""
Spider Silk Biomimesis: Molecular Hypergraph Architecture.
Based on Arg-Tyr coupling and Liquid-to-Liquid Phase Separation (LLPS).
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
        # Strength = cation charge * pi-cloud density
        strength = self.charge * other.pi_cloud if self.residue_type == 'R' else other.charge * self.pi_cloud
        return float(np.clip(strength, 0.0, 1.0))

class SpiderSilkHypergraph:
    """
    Model of spider silk dragline formation.
    The spider is a natural hypergraph engineer of x² = x + 1.
    """
    def __init__(self, n_nodes: int = 100):
        self.nodes: List[AminoAcidNode] = []
        self.bonds: List[Tuple[str, str, float]] = []

        # Populate with Arg and Tyr residues
        for i in range(n_nodes):
            res_type = 'R' if i % 2 == 0 else 'Y'
            self.nodes.append(AminoAcidNode(
                node_id=f"Res_{i}",
                residue_type=res_type,
                charge=0.9 if res_type == 'R' else 0.0,
                pi_cloud=0.85 if res_type == 'Y' else 0.0,
                coherence_C=0.3 # Low coherence in liquid dope
            ))

        self.global_C = 0.3
        self.global_F = 0.7

    def trigger_phase_separation(self, shear_force: float = 1.0) -> Dict[str, Any]:
        """
        Simulates the transition from liquid dope to solid fiber.
        (F high -> C high via LLPS).
        """
        print(f"🕷️ [SILK] Triggando separação de fases (Shear Force: {shear_force:.2f})")

        new_bonds = 0
        for i, node_a in enumerate(self.nodes):
            if not node_a.in_liquid_phase: continue
            for node_b in self.nodes[i+1:]:
                if not node_b.in_liquid_phase: continue

                strength = node_a.bond_strength(node_b)
                # Tension brings stickers together
                if strength * shear_force > 0.65:
                    self.bonds.append((node_a.node_id, node_b.node_id, strength))
                    node_a.in_liquid_phase = node_b.in_liquid_phase = False
                    # Coherence boost from structural order
                    node_a.coherence_C = node_b.coherence_C = 0.95
                    new_bonds += 1

        # Update global metrics
        solid_count = sum(1 for n in self.nodes if not n.in_liquid_phase)
        self.global_C = 0.3 + 0.7 * (solid_count / len(self.nodes))
        self.global_F = 1.0 - self.global_C

        return {
            "phase": "SOLID_FIBER" if self.global_C > 0.8 else "TRANSITIONING",
            "coherence": self.global_C,
            "fluctuation": self.global_F,
            "bonds": len(self.bonds)
        }

class AlzheimerProteinAggregation:
    """
    Contrast: Uncontrolled phase separation in neurodegeneration.
    """
    def __init__(self, n_nodes: int = 100):
        self.nodes = [{"id": i, "state": "HEALTHY", "C": 0.8} for i in range(n_nodes)]
        self.global_C = 0.8

    def simulate_stress(self, entropy_level: float = 0.5) -> Dict[str, Any]:
        """Simulates toxic aggregation (loss of C)."""
        print(f"🧠 [ALZHEIMER] Nível de estresse neural: {entropy_level:.2f}")

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
