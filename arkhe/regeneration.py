# arkhe/regeneration.py
"""
Neural Regeneration Logic: Long-distance communication in the neural hypergraph.
Based on the discovery of CCN1-mediated astrocyte-microglia coordination.
(Γ_regeneração)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class NeuralNode:
    """
    Representa um nó no hipergrafo neural.
    Pode ser um astrócito (coordenador), microglia (executor) ou neurônio.
    """
    node_id: str
    coherence_C: float
    fluctuation_F: float
    debris_level: float  # 0.0 a 1.0 (detritos lipídicos)
    role: str           # 'astrocyte', 'microglia', 'neuron'
    distance_from_origin: int = 0

    def update(self):
        """Garante a conservação de estado (simplificada)."""
        total = self.coherence_C + self.fluctuation_F + self.debris_level
        if total > 1.0:
            scale = 1.0 / total
            self.coherence_C *= scale
            self.fluctuation_F *= scale
            self.debris_level *= scale

class SpinalCordHypergraph:
    """
    Modelo de medula espinhal como hipergrafo segmentado.
    """
    def __init__(self, length_segments: int = 10, injury_start: int = 4, injury_end: int = 6):
        self.segments: List[NeuralNode] = []
        for i in range(length_segments):
            is_injured = injury_start <= i <= injury_end
            if is_injured:
                # Lesão: baixa coerência, alta flutuação e muitos detritos
                node = NeuralNode(
                    node_id=f"Seg_{i}_injured",
                    coherence_C=0.2,
                    fluctuation_F=0.6,
                    debris_level=0.8,
                    role='microglia' if i % 2 == 0 else 'neuron',
                    distance_from_origin=i
                )
            else:
                # Saudável: alta coerência, baixa flutuação
                node = NeuralNode(
                    node_id=f"Seg_{i}",
                    coherence_C=0.9,
                    fluctuation_F=0.1,
                    debris_level=0.05,
                    role='astrocyte' if i % 3 == 0 else 'neuron',
                    distance_from_origin=i
                )
            self.segments.append(node)

    def ccn1_handover(self, source_idx: int, target_idx: int) -> bool:
        """
        Handover Γ_CCN1: Astrócito distante instrui microglia na lesão.
        """
        if source_idx < 0 or source_idx >= len(self.segments) or \
           target_idx < 0 or target_idx >= len(self.segments):
            return False

        source = self.segments[source_idx]
        target = self.segments[target_idx]

        if source.role != 'astrocyte' or target.role != 'microglia':
            return False

        distance = abs(source.distance_from_origin - target.distance_from_origin)
        print(f"📡 [HANDOVER] Astrócito {source_idx} → Microglia {target_idx} (Distância: {distance})")

        # Ativação do nó executor via sinal de longa distância
        target.debris_level *= 0.3
        target.fluctuation_F *= 0.5
        target.coherence_C = min(1.0, target.coherence_C + 0.3)
        target.update()
        return True

class RegenerationTherapy:
    """
    Simula terapias baseadas em sinalização de longa distância.
    """
    def __init__(self, hypergraph: SpinalCordHypergraph):
        self.hg = hypergraph

    def apply_exogenous_ccn1(self, target_indices: List[int]):
        """Simula a administração de proteína CCN1 sintética."""
        print(f"💊 [THERAPY] Administrando CCN1 exógena nos segmentos {target_indices}...")
        for idx in target_indices:
            if idx < len(self.hg.segments):
                node = self.hg.segments[idx]
                if node.role == 'microglia':
                    print(f"   ✨ Microglia no segmento {idx} ativada exogenamente.")
                    node.debris_level *= 0.1
                    node.coherence_C = min(1.0, node.coherence_C + 0.5)
                    node.update()

    def run_natural_healing(self):
        """Simula o processo de cura natural via astrócitos distantes."""
        print("🌿 [NATURAL] Iniciando coordenação por astrócitos distantes...")
        astrocytes = [i for i, s in enumerate(self.hg.segments) if s.role == 'astrocyte' and s.coherence_C > 0.7]
        microglia = [i for i, s in enumerate(self.hg.segments) if s.role == 'microglia']

        for a_idx in astrocytes:
            for m_idx in microglia:
                self.hg.ccn1_handover(a_idx, m_idx)

    def get_status(self) -> Dict[str, Any]:
        avg_c = np.mean([s.coherence_C for s in self.hg.segments])
        avg_f = np.mean([s.fluctuation_F for s in self.hg.segments])
        total_debris = sum(s.debris_level for s in self.hg.segments)

        return {
            "avg_coherence": float(avg_c),
            "avg_fluctuation": float(avg_f),
            "total_debris": float(total_debris),
            "regenerative_state": "VIÁVEL" if total_debris < 0.5 else "COMPROMETIDA"
        }
