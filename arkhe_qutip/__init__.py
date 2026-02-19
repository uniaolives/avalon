"""
Arkhe-QuTiP: Quantum Hypergraph Toolbox
Extension of QuTiP for quantum hypergraph structures with Arkhe(N) coherence tracking.
"""

__version__ = "0.1.0"

from .core import ArkheQobj, ArkheSolver, HandoverEvent
from .hypergraph import QuantumHypergraph, Hyperedge, create_ring_hypergraph
from .coherence import (
    purity,
    von_neumann_entropy,
    coherence_l1,
    integrated_information
)
from .visualization import plot_hypergraph, plot_coherence_trajectory
from .chain_bridge import ArkheChainBridge

__all__ = [
    "ArkheQobj",
    "ArkheSolver",
    "HandoverEvent",
    "QuantumHypergraph",
    "Hyperedge",
    "create_ring_hypergraph",
    "purity",
    "von_neumann_entropy",
    "coherence_l1",
    "integrated_information",
    "plot_hypergraph",
    "plot_coherence_trajectory",
    "ArkheChainBridge"
]
