# arkhe/consensus.py
"""
Proof-of-Syzygy Consensus (Γ_syzygy)
Consensus mechanism based on nodes α, β, γ and their coherence states.
"""

from typing import List, Dict, Any, Tuple
import numpy as np

class SyzygyConsensus:
    """
    Motor de Consenso Proof-of-Syzygy.
    Valida handovers e mudanças de estado via votação ponderada por Coerência (C).
    """
    def __init__(self, voting_threshold: float = 0.67):
        self.voting_threshold = voting_threshold # 2/3 majority
        self.node_roles = {
            0: "α (Alpha)",
            1: "β (Beta)",
            2: "γ (Gamma)"
        }

    def validate_handover(self, nodes_subset: List[Any], proposed_change: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Realiza a votação entre os nós internos (α, β, γ).
        Apenas os nós α, β e γ (IDs 0, 1, 2) são considerados validadores.
        """
        votes = []
        total_coherence = 0.0
        weighted_approval = 0.0

        print(f"⚖️ [CONSENSUS] Iniciando votação Proof-of-Syzygy para: {proposed_change}")

        # Filtrar apenas os validadores do subset fornecido
        validators = [n for n in nodes_subset if n.id in self.node_roles]

        if not validators:
            return False, {"reason": "Nenhum validador α, β, γ presente no subset."}

        for node in validators:
            role = self.node_roles[node.id]
            # No Arkhe, a aprovação é dada se a Coerência individual C > 0.85
            # Mas o voto é ponderado pela própria Coerência
            approved = node.C > 0.85
            total_coherence += node.C

            if approved:
                weighted_approval += node.C

            votes.append({
                "id": node.id,
                "role": role,
                "coherence": node.C,
                "vote": "APPROVE" if approved else "REJECT"
            })
            print(f"   • {role}: {votes[-1]['vote']} (C={node.C:.4f})")

        # Threshold check
        consensus_score = weighted_approval / max(total_coherence, 0.0001)
        is_validated = consensus_score >= self.voting_threshold

        result = {
            "is_validated": is_validated,
            "consensus_score": float(consensus_score),
            "threshold": self.voting_threshold,
            "votes": votes
        }

        if is_validated:
            print(f"✅ [CONSENSUS] Handover validado! Score: {consensus_score:.2f}")
        else:
            print(f"❌ [CONSENSUS] Handover rejeitado. Score: {consensus_score:.2f}")

        return is_validated, result
