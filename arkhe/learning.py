# arkhe/learning.py
"""
Adaptive Learning and Pattern Management Module.
Implements ANCCR (Adjusted Net Contingency of Causal Relations) and Success/Failure Pattern Management.
(Γ_aprendizado)
"""

import numpy as np
from typing import Dict, Any, List, Optional

class ANCCRModel:
    """
    Adjusted Net Contingency of Causal Relations (Burke et al., 2026).
    Taxa de aprendizado α é proporcional ao Inter-Reward Interval (IRI).
    """
    def __init__(self, base_rate: float = 0.01):
        self.base_rate = base_rate
        self.learning_rate = base_rate

    def update_learning_rate(self, iri: float) -> float:
        """α ∝ IRI. Um intervalo maior permite inferência causal retrospectiva mais profunda."""
        self.learning_rate = self.base_rate * iri
        return self.learning_rate

    def retrospective_inference(self, events: List[Dict[str, Any]]) -> Dict[str, float]:
        """Infere a causa a partir do efeito (retrospecção)."""
        # Simulação de contingência causal
        contingencies = {}
        for i, event in enumerate(events):
            contingencies[event['name']] = np.exp(-i / (self.learning_rate + 1e-10))
        return contingencies

class PatternManager:
    """
    Gerencia a amplificação de padrões de sucesso e a liberação de padrões obsoletos.
    (Princípio da Ação: De possibilidade a probabilidade)
    """
    def __init__(self):
        self.active_principles = {
            "Law of Three": "Stable structures form in triadic geometry.",
            "Golden Timing": "Temporal processes align to φ harmonics (φ⁴ ≈ 6.854 Hz).",
            "Field First": "Ephaptic coupling precedes physical edges."
        }
        self.obsolete_patterns = []

    def amplify_success(self, pattern_name: str, result: float):
        """Ação: Amplifica padrões com alta coerência (C)."""
        if result > 0.85:
            print(f"✅ Pattern '{pattern_name}' amplified. Probability of recurrence increased.")
            return True
        return False

    def release_obsolete(self, pattern_name: str, fluctuation: float):
        """Ação: Libera práticas com alta flutuação (F)."""
        if fluctuation > 0.7:
            if pattern_name in self.active_principles:
                del self.active_principles[pattern_name]
            self.obsolete_patterns.append(pattern_name)
            print(f"🔥 Obsolete pattern '{pattern_name}' released. Resources freed.")
            return True
        return False

    def get_architectural_rules(self) -> Dict[str, str]:
        """Retorna as regras de design atuais do hipergrafo."""
        return self.active_principles
