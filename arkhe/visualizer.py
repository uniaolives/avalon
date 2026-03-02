# arkhe/visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from arkhe.memory import CortexMemory

class ArkheViz:
    """
    Visualizador de Densidade de Conhecimento (Γ_viz).
    Mapeia a gravidade semântica e a topologia do Córtex do Arkhe.
    Agora inclui status de Soberania de Infraestrutura (TEE).
    """
    def __init__(self, memory: CortexMemory, registry: Optional[Any] = None):
        self.memory = memory
        self.registry = registry

    def analyze_topology(self, perplexity: int = 30) -> Dict[str, Any]:
        """
        Análise completa da topologia do conhecimento.
        """
        print("🔭 Analisando topologia do córtex...")

        # 1. Extração de dados
        data = self.memory.insights.get(include=['embeddings', 'metadatas', 'documents'])
        ids = data['ids']
        embeddings = np.array(data['embeddings'])
        metadatas = data['metadatas']

        n_nodes = len(ids)
        if n_nodes < 3:
            return {"status": "insufficient_data"}

        # 2. Redução dimensional (t-SNE)
        tsne = TSNE(
            n_components=2,
            perplexity=min(perplexity, n_nodes-1),
            init='pca',
            learning_rate='auto',
            random_state=42
        )
        coords_2d = tsne.fit_transform(embeddings)

        # 3. Construção do grafo semântico
        G = nx.Graph()
        for i, node_id in enumerate(ids):
            topic = metadatas[i].get('topic', 'Unknown')
            # Marcar soberania (se o nó de origem estiver no registro e atestado)
            source_node = metadatas[i].get('source_node', 'Unknown')
            is_sovereign = False
            if self.registry and source_node in self.registry.nodes:
                is_sovereign = self.registry.nodes[source_node].is_attested

            G.add_node(node_id, pos=coords_2d[i], topic=topic, is_sovereign=is_sovereign)

            # Arestas por similaridade de cosseno
            for j in range(i+1, n_nodes):
                sim = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]) + 1e-6
                )
                if sim > 0.6:
                    G.add_edge(node_id, ids[j], weight=float(sim))

        # 4. Detecção de comunidades
        try:
            communities = nx.community.greedy_modularity_communities(G)
        except Exception:
            communities = [{node} for node in G.nodes()]

        cluster_map = {}
        for i, community in enumerate(communities):
            for node in community:
                cluster_map[node] = i

        centrality = nx.degree_centrality(G)

        return {
            "status": "success",
            "ids": ids,
            "coords": coords_2d,
            "graph": G,
            "cluster_map": cluster_map,
            "communities": communities,
            "centrality": centrality,
            "metadatas": metadatas
        }

    def generate_map(self, output_path: str = "arkhe_semantic_map.png"):
        """
        Gera o mapa visual de gravidade semântica com 4 subplots.
        """
        topology = self.analyze_topology()
        if topology["status"] != "success":
            print("⚠️ Memória insuficiente para gerar mapa complexo.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"ARKHE(n) OS — Mapa de Gravidade Semântica (Γ_viz)", fontsize=16, fontweight='bold')

        G = topology["graph"]
        pos = nx.get_node_attributes(G, 'pos')
        cluster_map = topology["cluster_map"]

        # 1. Mapa de Densidade Principal com Marcadores de Soberania
        ax1 = axes[0, 0]
        node_colors = [cluster_map.get(n, 0) for n in G.nodes()]
        d = dict(G.degree)
        max_deg = max(d.values()) if d and max(d.values()) > 0 else 1
        node_sizes = [(v / max_deg) * 500 + 100 for v in d.values()]

        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors,
                               cmap=plt.cm.tab10, alpha=0.7, ax=ax1)

        # Adicionar "escudos" para nós soberanos
        sovereign_nodes = [n for n, attr in G.nodes(data=True) if attr.get('is_sovereign')]
        if sovereign_nodes:
            sov_pos = {n: pos[n] for n in sovereign_nodes}
            nx.draw_networkx_nodes(G, sov_pos, node_size=[s*1.5 for s, n in zip(node_sizes, G.nodes()) if n in sovereign_nodes],
                                   node_color='none', edgecolors='gold', linewidths=2, ax=ax1)

        nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color='gray', ax=ax1)

        avg_deg = np.mean(list(d.values())) if d else 0
        labels = {n: G.nodes[n]['topic'] for n in G.nodes if d[n] >= avg_deg}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax1,
                                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        ax1.set_title("Gravidade Semântica (Escudo Dourado = Soberano/TEE)")
        ax1.axis('off')

        # 2. Status de Soberania da Infraestrutura
        ax2 = axes[0, 1]
        sov_count = len(sovereign_nodes)
        vuln_count = len(G.nodes()) - sov_count
        ax2.pie([sov_count, vuln_count], labels=['Soberano (TEE)', 'Vulnerável'],
                autopct='%1.1f%%', colors=['gold', 'lightgray'], startangle=90)
        ax2.set_title("Composição do Substrato de Infraestrutura")

        # 3. Conexões entre Clusters (Bridges)
        ax3 = axes[1, 0]
        bridges = defaultdict(float)
        for u, v, data in G.edges(data=True):
            c1, c2 = cluster_map[u], cluster_map[v]
            if c1 != c2:
                pair = tuple(sorted((c1, c2)))
                bridges[pair] += data.get('weight', 1.0)

        if bridges:
            b_pairs = [f"C{p[0]}↔C{p[1]}" for p in bridges.keys()]
            b_weights = list(bridges.values())
            ax3.barh(b_pairs, b_weights, color='orange')
            ax3.set_xlabel("Força da Ponte")
            ax3.set_title("Pontes Transdisciplinares")
        else:
            ax3.text(0.5, 0.5, "Sem pontes detectadas", ha='center')

        # 4. Distribuição de Centralidade
        ax4 = axes[1, 1]
        centralities = list(topology["centrality"].values())
        ax4.hist(centralities, bins=15, color='skyblue', edgecolor='black')
        ax4.set_xlabel("Centralidade de Grau")
        ax4.set_ylabel("Frequência")
        ax4.set_title("Hierarquia do Conhecimento")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(output_path)
        print(f"✅ Mapa soberano salvo em: {output_path}")
        return topology
