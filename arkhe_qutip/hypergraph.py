import numpy as np
import qutip as qt
from typing import List, Dict, Any, Tuple, Optional
from .core import ArkheQobj

class Hyperedge:
    """Represents a multi-qubit operator connecting nodes in the hypergraph."""
    def __init__(self, nodes: Tuple[int, ...], operator: qt.Qobj, weight: float = 1.0):
        self.nodes = nodes
        self.operator = operator
        self.weight = weight

    def __repr__(self):
        return f"Hyperedge(nodes={self.nodes}, weight={self.weight})"

class QuantumHypergraph:
    """
    Structure representing a network of quantum states connected by hyperedges.
    """
    def __init__(self, nodes: List[ArkheQobj] = None, name: str = "QuantumHypergraph"):
        self.nodes = nodes or []
        self.hyperedges: List[Hyperedge] = []
        self.name = name

    @property
    def n_nodes(self) -> int:
        return len(self.nodes)

    @property
    def n_hyperedges(self) -> int:
        return len(self.hyperedges)

    @property
    def global_coherence(self) -> float:
        """Calculates the average coherence of all nodes."""
        if not self.nodes:
            return 0.0
        return np.mean([node.coherence for node in self.nodes])

    def add_node(self, node: ArkheQobj):
        self.nodes.append(node)

    def add_hyperedge(self, nodes: Tuple[int, ...], operator: qt.Qobj, weight: float = 1.0):
        self.hyperedges.append(Hyperedge(nodes, operator, weight))

    def add_two_qubit_gate(self, i: int, j: int, operator: qt.Qobj, weight: float = 1.0):
        self.add_hyperedge((i, j), operator, weight)

    def get_topology_stats(self) -> Dict[str, Any]:
        """Returns statistics about the hypergraph topology."""
        return {
            "n_nodes": self.n_nodes,
            "n_hyperedges": self.n_hyperedges,
            "density": self.n_hyperedges / (self.n_nodes * (self.n_nodes - 1) / 2) if self.n_nodes > 1 else 0,
            "global_coherence": self.global_coherence
        }

    def to_networkx(self):
        """Converts the hypergraph to a NetworkX graph (simplified)."""
        import networkx as nx
        G = nx.Graph()
        for i, node in enumerate(self.nodes):
            G.add_node(i, coherence=node.coherence)
        for edge in self.hyperedges:
            if len(edge.nodes) == 2:
                G.add_edge(edge.nodes[0], edge.nodes[1], weight=edge.weight)
            else:
                # For hyperedges > 2, we can represent as a clique or a special node
                for i in range(len(edge.nodes)):
                    for j in range(i + 1, len(edge.nodes)):
                        G.add_edge(edge.nodes[i], edge.nodes[j], weight=edge.weight)
        return G

    def __str__(self):
        return f"QuantumHypergraph('{self.name}', nodes={self.n_nodes}, edges={self.n_hyperedges}, C={self.global_coherence:.4f})"

def create_ring_hypergraph(n: int) -> QuantumHypergraph:
    """Creates a ring topology of n qubits."""
    hg = QuantumHypergraph(name=f"Ring-{n}")
    for i in range(n):
        hg.add_node(ArkheQobj(qt.basis(2, 0)))

    # Add CNOT between adjacent nodes
    cnot = qt.Qobj([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dims=[[2,2],[2,2]])
    for i in range(n):
        hg.add_two_qubit_gate(i, (i + 1) % n, cnot)

    return hg
