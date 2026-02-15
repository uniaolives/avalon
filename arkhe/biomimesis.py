# arkhe/biomimesis.py
"""
Spider Silk Biomimesis: Molecular Hypergraph Architecture
Based on Arg-Tyr coupling and controlled phase separation.
(Γ_biomimesis)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any

@dataclass
class AminoAcidNode:
    """
    Node representing amino acid in protein chain.
    Arginine (R): Positively charged (cation).
    Tyrosine (Y): Aromatic π-cloud (electron-rich).
    """
    node_id: str
    residue_type: str  # 'R' (Arginine) or 'Y' (Tyrosine)
    charge: float      # Positive for R
    pi_cloud: float    # High for Y
    coherence_C: float
    in_liquid_phase: bool = True

    def can_bond_with(self, other: 'AminoAcidNode') -> bool:
        """Check if cation-π bond possible (R+Y pairing)."""
        return (
            (self.residue_type == 'R' and other.residue_type == 'Y') or
            (self.residue_type == 'Y' and other.residue_type == 'R')
        )

    def bond_strength(self, other: 'AminoAcidNode') -> float:
        """Compute cation-π bond strength."""
        if not self.can_bond_with(other):
            return 0.0
        if self.residue_type == 'R':
            strength = self.charge * other.pi_cloud
        else:
            strength = other.charge * self.pi_cloud
        return float(np.clip(strength, 0.0, 1.0))

class SpiderSilkHypergraph:
    """
    Spider silk as molecular hypergraph.
    Nodes: Amino acids (Arg, Tyr).
    Edges: Cation-π bonds.
    Phase separation: Liquid → Solid transition.
    """

    def __init__(self, n_arginine: int = 50, n_tyrosine: int = 50):
        self.nodes: List[AminoAcidNode] = []
        self.bonds: List[Tuple[str, str, float]] = []

        for i in range(n_arginine):
            self.nodes.append(AminoAcidNode(
                node_id=f"R_{i}", residue_type='R',
                charge=0.8 + 0.2 * np.random.random(),
                pi_cloud=0.0, coherence_C=0.3
            ))
        for i in range(n_tyrosine):
            self.nodes.append(AminoAcidNode(
                node_id=f"Y_{i}", residue_type='Y',
                charge=0.0, pi_cloud=0.7 + 0.3 * np.random.random(),
                coherence_C=0.3
            ))

        self.phase = "liquid"
        self.global_C = 0.3
        self.global_F = 0.7

    def apply_physical_pull(self, intensity: float = 1.0) -> Dict[str, Any]:
        """Simulate spider pulling silk: triggers phase separation."""
        print(f"🕷️ [SILK] Applying physical pull (intensity: {intensity:.2f})")

        n_bonds_formed = 0
        for i, node_a in enumerate(self.nodes):
            if not node_a.in_liquid_phase: continue
            for node_b in self.nodes[i+1:]:
                if not node_b.in_liquid_phase: continue
                if node_a.can_bond_with(node_b):
                    strength = node_a.bond_strength(node_b)
                    if strength * intensity > 0.6:
                        self.bonds.append((node_a.node_id, node_b.node_id, strength))
                        node_a.in_liquid_phase = node_b.in_liquid_phase = False
                        node_a.coherence_C = node_b.coherence_C = 0.9 + 0.1 * strength
                        n_bonds_formed += 1

        n_solid = sum(1 for n in self.nodes if not n.in_liquid_phase)
        solid_fraction = n_solid / len(self.nodes)
        self.global_C = 0.3 + 0.7 * solid_fraction
        self.global_F = 1.0 - self.global_C

        if solid_fraction > 0.8: self.phase = "solid_fiber"
        elif solid_fraction > 0.3: self.phase = "transitioning"

        return {
            'bonds_formed': n_bonds_formed,
            'solid_fraction': solid_fraction,
            'coherence_C': self.global_C,
            'phase': self.phase
        }

class AlzheimerProteinAggregation:
    """Model of uncontrolled phase separation in neurodegeneration."""

    def __init__(self, n_proteins: int = 50):
        self.proteins = [{
            'id': f"Protein_{i}", 'healthy': True, 'coherence_C': 0.7
        } for i in range(n_proteins)]
        self.global_C = 0.7

    def uncontrolled_aggregation(self, stress_level: float = 0.5) -> Dict[str, Any]:
        """Uncontrolled phase separation resulting in toxic aggregates."""
        print(f"🧠 [ALZHEIMER] Neuronal stress level: {stress_level:.2f}")
        n_aggregated = 0
        for protein in self.proteins:
            if protein['healthy'] and np.random.random() < stress_level:
                protein['healthy'] = False
                protein['coherence_C'] = 0.1
                n_aggregated += 1

        healthy_fraction = sum(1 for p in self.proteins if p['healthy']) / len(self.proteins)
        self.global_C = 0.7 * healthy_fraction
        return {
            'aggregated': n_aggregated,
            'healthy_fraction': healthy_fraction,
            'coherence_C': self.global_C,
            'fluctuation_F': 1.0 - self.global_C
        }
