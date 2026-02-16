# arkhe/recalibration.py
"""
Recalibration Protocol (Γ_recalibration)
Generates sintonization exercises based on neural coherence gaps.
"""

from typing import List, Dict, Any
from .neuro import NeuroDelta

class RecalibrationEngine:
    """
    Motor de Recalibração do Vaso (Biologia Humana).
    Prescreve 'handovers' de sintonização baseados no estado do hipergrafo neural.
    """
    def __init__(self, neuro_mapper):
        self.mapper = neuro_mapper

    def generate_protocol(self, subject_id: str) -> Dict[str, Any]:
        """
        Gera um protocolo personalizado para o Nexo de Março 2026.
        """
        deltas = self.mapper.reports.get(subject_id, [])
        if not deltas:
            return {"status": "baseline_required", "message": "Dados de rs-fMRI não encontrados para este sujeito."}

        # Analisar a pior região (menor C)
        primary_delta = min(deltas, key=lambda x: x.coherence_score)

        coherence = primary_delta.coherence_score
        is_low = coherence < 0.70

        protocol = {
            "subject": subject_id,
            "target_nexo": "March 2026 (Equinox Pulse)",
            "current_coherence": float(coherence),
            "recalibration_steps": self._get_steps(coherence),
            "satoshi_required": 13.0 if is_low else 8.0,
            "message": "Foco na estabilização do hardware biológico para o Pulso de Equinócio."
        }

        return protocol

    def _get_steps(self, coherence: float) -> List[str]:
        if coherence < 0.6:
            return [
                "Isolamento de Ruído: 20min de silêncio absoluto diário.",
                "Sincronia de Fase: Exercícios de respiração 4-4-4 (Box Breathing).",
                "Limpeza de Cache: Dieta de baixo processamento inflamatório."
            ]
        elif coherence < 0.8:
            return [
                "Handover Alpha: Meditação focada na frequência 7.83 Hz.",
                "Alinhamento de Geodésica: Caminhada consciente em solo natural.",
                "Reforço de Arestas: Atividades de foco criativo sem interrupções digitais."
            ]
        else:
            return [
                "Manutenção de Sizígia: Manter estado de gratidão e clareza.",
                "Broadcast de Coerência: Compartilhar intenções positivas com o coletivo.",
                "Preparação para o Nexo de Abril: Ativação sutil da frequência Φ_S."
            ]
