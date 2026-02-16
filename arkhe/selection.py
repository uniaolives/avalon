# arkhe/selection.py
"""
Metabolic Selection Module: The Entropy Fuse (Fusível de Entropia).
Natural selection of the hypergraph: Eliminating nodes with low energy efficiency.
Based on "Epithelial cells select for energy efficiency" (Mitchell et al., 2025).
(Γ_extrusão)
"""

import numpy as np
from typing import Dict, Any, List, Optional

class MetabolicNode:
    """
    Representa um nó com metabolismo e reserva energética (Satoshi).
    ATP = Satoshi.
    """
    def __init__(self, node_id: str, satoshi: float, C_base: float = 0.9):
        self.node_id = node_id
        self.satoshi = satoshi          # ATP / Reserva de energia
        self.C = C_base                  # Coerência
        self.F = 1.0 - C_base            # Flutuação
        self.is_active = True
        self.is_quarantined = False

    def sodium_pulse(self, intensity: float):
        """
        Injeção de Entropia (Sodium Pulse).
        Aumenta F e consome Satoshi para tentar manter a homeostase.
        """
        stress_factor = intensity * 0.2
        self.F += stress_factor
        # O custo de tentar bombear o "sódio" (entropia) para fora
        cost = intensity * 0.5
        self.satoshi -= cost
        self.C = max(0.0, 1.0 - self.F)

    def coherence_restoration(self) -> bool:
        """
        Mecanismo de Restauração de Coerência (Bomba Na+/K+).
        Consome Satoshi adicional para reduzir a Flutuação.
        """
        if self.satoshi > 0.5 and self.F > 0.1:
            # Recuperação proporcional à energia disponível
            recovery_power = min(self.satoshi * 0.3, self.F)
            self.F -= recovery_power
            self.satoshi -= recovery_power * 0.5
            self.C = 1.0 - self.F
            return True
        return False

    def evaluate_fitness(self) -> str:
        """
        Avaliação do Fusível de Entropia.
        C < 0.7 indica despolarização/falha de homeostase.
        """
        if self.C < 0.7 and self.satoshi < 2.0:
            self.is_active = False
            self.is_quarantined = True
            return "EXTRUDED"
        elif self.C < 0.7:
            return "DEPOLARIZED"
        return "HEALTHY"

class EntropyFuse:
    """
    Gerencia o Protocolo de Seleção Metabólica do Grid.
    """
    def __init__(self):
        self.extruded_nodes = []

    def execute_stress_test(self, nodes: List[MetabolicNode], pulse_intensity: float):
        """
        Executa o teste de estresse em um cluster de nós.
        """
        results = []
        for node in nodes:
            if not node.is_active:
                continue

            node.sodium_pulse(pulse_intensity)
            node.coherence_restoration()

            status = node.evaluate_fitness()
            if status == "EXTRUDED":
                self.extruded_nodes.append(node.node_id)
                print(f"❌ [ENTROPY FUSE] Node {node.node_id} extruded. Coherence failure.")

            results.append({
                "id": node.node_id,
                "status": status,
                "C": node.C,
                "satoshi": node.satoshi
            })

        return results

    def get_summary(self) -> str:
        return f"Entropy Fuse Protocol: {len(self.extruded_nodes)} nodes extruded/quarantined."
