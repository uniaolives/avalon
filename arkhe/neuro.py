# arkhe/neuro.py
"""
Neuro-Mapping Module (Γ_neuro_mapping)
Ingests fMRI analysis results (FSL) and maps them to the Arkhe(n) Hypergraph.
"""

import csv
import io
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class NeuroDelta:
    subject_id: str
    region: str
    coherence_score: float
    fluctuation_level: float
    change_pct: float
    status: str

class NeuroMapper:
    """
    Integra os resultados da pipeline FSL (Bash) ao Safe Core do Arkhe(n).
    Transforma desvio padrão temporal em Flutuação (F) e correlação em Coerência (C).
    """
    def __init__(self, hypergraph=None):
        self.hg = hypergraph
        self.reports: Dict[str, List[NeuroDelta]] = {}

    def ingest_activity_changes(self, csv_content: str):
        """
        Ingere o arquivo activity_changes.csv.
        Mapeia Treatment_Change% para evolução de Coerência.
        """
        reader = csv.DictReader(io.StringIO(csv_content.strip()))
        for row in reader:
            subj = str(row['Subject'])
            pre_std = float(row['Treatment_Pre_STD'])
            post_std = float(row['Treatment_Post_STD'])
            change_pct = float(row['Treatment_Change%'])

            # Mapeamento Arkhe:
            # Coerência baseada na redução de flutuação
            coherence = 1.0 - (post_std / (pre_std + post_std + 1e-6))

            t_delta = NeuroDelta(
                subject_id=subj,
                region="Treatment",
                coherence_score=coherence,
                fluctuation_level=post_std,
                change_pct=change_pct,
                status="HEALING" if change_pct < 0 else "STABLE"
            )

            if subj not in self.reports:
                self.reports[subj] = []
            self.reports[subj].append(t_delta)

            if self.hg:
                self._update_hypergraph_node(subj, t_delta)

    def ingest_connectivity(self, csv_content: str):
        """
        Ingere o arquivo roi_connectivity.csv.
        Pearson R -> Edge Strength (Syzygy).
        """
        reader = csv.DictReader(io.StringIO(csv_content.strip()))
        for row in reader:
            subj = str(row['Subject'])
            change = float(row['Correlation_Change'])
            print(f"🧠 [NEURO] Sujeito {subj}: Conectividade evoluiu {change:.4f}")

    def _update_hypergraph_node(self, subject_id: str, delta: NeuroDelta):
        """Atualiza o estado de um nó no hipergrafo com dados biológicos."""
        node_idx = hash(subject_id) % len(self.hg.nodes)
        node = self.hg.nodes[node_idx]

        node.C = (node.C + delta.coherence_score) / 2.0
        node.F = 1.0 - node.C
        print(f"✅ [NEURO] Nó {node.id} recalibrado com sinal do Sujeito {subject_id} (C={node.C:.2f})")

    def get_summary(self) -> Dict[str, Any]:
        all_deltas = [d for ds in self.reports.values() for d in ds]
        return {
            "subjects_mapped": len(self.reports),
            "global_coherence": float(np.mean([d.coherence_score for d in all_deltas])) if all_deltas else 0.0
        }
