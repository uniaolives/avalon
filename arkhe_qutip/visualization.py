import numpy as np
from typing import List, Dict, Any, Optional

def plot_hypergraph(hg: Any, layout: str = 'spring', ax: Optional[Any] = None):
    """
    Plots the quantum hypergraph using NetworkX and Matplotlib.
    Nodes are colored by their coherence.
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError:
        print("Visualization requires matplotlib and networkx. Please install them.")
        return None, None

    G = hg.to_networkx()

    if layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G)

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    # Get coherence values for coloring
    coherences = [G.nodes[i]['coherence'] for i in G.nodes]

    nx.draw_networkx_nodes(G, pos, node_color=coherences, cmap='viridis',
                           node_size=500, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    ax.set_title(f"Quantum Hypergraph: {hg.name}")
    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label="Coherence (Purity)")

    return plt.gcf(), ax

def plot_coherence_trajectory(trajectory: List[float], tlist: Optional[np.ndarray] = None,
                             events: Optional[List[Any]] = None, ax: Optional[Any] = None):
    """
    Plots the evolution of coherence over time.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Visualization requires matplotlib. Please install it.")
        return None, None

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    x = tlist if tlist is not None else np.arange(len(trajectory))
    ax.plot(x, trajectory, lw=2, label="Coherence")

    if events:
        # Mark handover events
        for event in events:
            if hasattr(event, 'timestamp'):
                pass

    ax.set_xlabel("Time / Step")
    ax.set_ylabel("Coherence (Purity)")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    return plt.gcf(), ax
