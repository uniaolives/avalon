# papercoder_kernel/core/als_model.py
"""
ALS Hypergraph Node Model (Γ_als).
Hypothetical model of motor neuron degeneration as hypergraph decoherence.
"""

import random
from typing import List, Optional

class ALS_Node:
    """
    Um neurônio motor modelado como nó do hipergrafo.
    Integra riscos genéticos (SOD1, C9orf72) e estresse ambiental.
    """
    def __init__(self, node_id: str, genetic_risk: float = 0.0, environmental_exposure: float = 0.0):
        self.id = node_id
        self.coherence = 1.0           # Começa em estado de syzygy total
        self.sod1_mutation = genetic_risk
        self.c9orf72_loops = 0
        self.oxidative_stress = 0.0
        self.env = environmental_exposure
        self.is_alive = True

    def step(self):
        """Simula um passo temporal na progressão da doença."""
        if not self.is_alive:
            return False

        # 1. Estresse oxidativo cresce com exposição e mutações
        self.oxidative_stress += 0.01 * (self.env + self.sod1_mutation)

        # 2. Expansões C9orf72 ocorrem estocasticamente
        if random.random() < 0.001 * self.sod1_mutation:
            self.c9orf72_loops += 1

        # 3. Coerência (C) cai conforme a hesitação (F) aumenta via estresse
        # O modelo Arkhe diz C + F = 1. Aqui, F é induzido pela patologia.
        decoherence_rate = (0.005 * self.oxidative_stress + 0.01 * self.c9orf72_loops)
        self.coherence -= decoherence_rate

        # 4. Ponto crítico de hesitação (Φ_crit = 0.15 no tratado)
        # Quando a coerência cai abaixo de um limiar, o nó entra em colapso.
        if self.coherence < 0.2:
            self.is_alive = False
            return False

        return True

class ALS_Hypergraph:
    """Um sub-hipergrafo representando uma população de neurônios motores."""
    def __init__(self, n_nodes: int, risk_profile: float = 0.1):
        self.nodes = [
            ALS_Node(f"MN_{i}", genetic_risk=risk_profile * random.random(), environmental_exposure=0.05)
            for i in range(n_nodes)
        ]

    def simulate_step(self):
        """Executa um passo para toda a rede."""
        for node in self.nodes:
            node.step()

    def get_global_coherence(self) -> float:
        """Calcula a coerência média da rede."""
        alive_nodes = [n for n in self.nodes if n.is_alive]
        if not alive_nodes:
            return 0.0
        return sum(n.coherence for n in alive_nodes) / len(self.nodes)

    def get_survival_rate(self) -> float:
        """Retorna a porcentagem de nós vivos."""
        alive_count = sum(1 for n in self.nodes if n.is_alive)
        return alive_count / len(self.nodes)
