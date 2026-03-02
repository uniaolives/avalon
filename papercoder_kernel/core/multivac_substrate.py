# papercoder_kernel/core/multivac_substrate.py
"""
Multivac Computational Substrate (Γ_substrate).
Aggregates heterogeneous nodes into a unified execution manifold.
"""

import numpy as np
from typing import Dict, List, Optional

class ComputeNode:
    """Um nó de processamento no substrato Multivac."""
    def __init__(self, node_id: str, compute_capacity: float, memory: float,
                 coherence: float, location: tuple, node_type: str):
        self.node_id = node_id
        self.compute_capacity = compute_capacity
        self.memory = memory
        self.coherence = coherence
        self.location = location
        self.node_type = node_type

class MultivacSubstrate:
    """O substrato global que gerencia os recursos computacionais."""
    def __init__(self):
        self.nodes: Dict[str, ComputeNode] = {}

    def register_node(self, node: ComputeNode):
        self.nodes[node.node_id] = node

    @property
    def total_capacity(self) -> float:
        return sum(n.compute_capacity for n in self.nodes.values())

    @property
    def global_coherence(self) -> float:
        if not self.nodes:
            return 0.0
        return sum(n.coherence for n in self.nodes.values()) / len(self.nodes)

    def measure_entropy(self) -> float:
        """S = 1 - C (Entropia local do sistema)"""
        return 1.0 - self.global_coherence

    def allocate_computation(self, complexity: float, required_coherence: float) -> List[str]:
        """Aloca nós que satisfaçam o requisito de coerência."""
        # Seleciona nós com coerência suficiente
        valid_nodes = [nid for nid, n in self.nodes.items() if n.coherence >= required_coherence]
        return valid_nodes
