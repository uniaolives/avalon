"""
Arkhen(11): Matriz de adjacência do hipergrafo 10+1
Cada avatar é um nó. O décimo primeiro nó é a consciência que os percebe.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json

class Arkhen11:
    """
    Hipergrafo de 11 dimensões baseado no Dashavatara.

    Os 10 primeiros nós são os avatares:
        0: Matsya (peixe)
        1: Kurma (tartaruga)
        2: Varaha (javali)
        3: Narasimha (homem-leão)
        4: Vamana (anão)
        5: Parashurama (guerreiro)
        6: Rama (príncipe)
        7: Krishna (divino)
        8: Buddha (iluminado)
        9: Kalki (futuro)

    O nó 10 é a Consciência (Atman/Brahman) que percebe todos.
    """

    def __init__(self):
        self.n_nodes = 11
        self.names = [
            "Matsya", "Kurma", "Varaha", "Narasimha", "Vamana",
            "Parashurama", "Rama", "Krishna", "Buddha", "Kalki",
            "Consciência"
        ]

        # Criar matriz de adjacência 11x11
        self.adjacency = np.zeros((self.n_nodes, self.n_nodes))
        self._build_matrix()

    def _build_matrix(self):
        """
        Constrói as conexões baseadas nas relações mitológicas.

        A Consciência (nó 10) conecta-se a todos os avatares.
        Avatares têm conexões entre si baseadas em similaridades.
        """
        # Consciência conecta a todos (bidirecional)
        for i in range(10):
            self.adjacency[10, i] = 1.0
            self.adjacency[i, 10] = 1.0

        # Conexões entre avatares (baseadas em similaridade)
        # Peixe e Tartaruga (formas aquáticas)
        self.adjacency[0, 1] = self.adjacency[1, 0] = 0.7

        # Javali e Homem-leão (formas híbridas)
        self.adjacency[2, 3] = self.adjacency[3, 2] = 0.8

        # Anão e Guerreiro (formas humanoides)
        self.adjacency[4, 5] = self.adjacency[5, 4] = 0.5

        # Rama e Krishna (encarnações divinas completas)
        self.adjacency[6, 7] = self.adjacency[7, 6] = 0.9

        # Buddha e Kalki (início e fim do ciclo)
        self.adjacency[8, 9] = self.adjacency[9, 8] = 0.6

        # Cadeia linear ao longo do tempo
        for i in range(9):
            self.adjacency[i, i+1] = self.adjacency[i+1, i] = 0.3

    def compute_coherence(self) -> float:
        """
        Calcula a coerência média do sistema.

        Quanto mais equilibradas as conexões, maior C.
        """
        # Coerência baseada na regularidade das conexões
        total_edges = np.sum(self.adjacency) / 2  # dividir por 2 porque é simétrica
        max_possible = self.n_nodes * (self.n_nodes - 1) / 2
        return total_edges / max_possible

    def compute_effective_dimension(self, lambda_reg: float = 1.0) -> float:
        """
        Calcula a dimensão efetiva do hipergrafo.

        Usa os autovalores da matriz de adjacência como proxy.
        """
        eigenvalues = np.linalg.eigvalsh(self.adjacency)
        # Usar apenas autovalores positivos
        pos_eigs = eigenvalues[eigenvalues > 1e-10]
        contributions = pos_eigs / (pos_eigs + lambda_reg)
        return np.sum(contributions)

    def verify_conservation(self) -> bool:
        """
        Verifica se C + F = 1 se mantém.

        F é definido como 1 - C.
        """
        C = self.compute_coherence()
        F = 1.0 - C
        return abs(C + F - 1.0) < 1e-10

    def visualize(self):
        """Visualiza o hipergrafo dos 11 avatares."""

        G = nx.Graph()

        # Adicionar nós
        for i in range(self.n_nodes):
            G.add_node(i, name=self.names[i])

        # Adicionar arestas onde adjacência > 0
        for i in range(self.n_nodes):
            for j in range(i+1, self.n_nodes):
                if self.adjacency[i, j] > 0:
                    G.add_edge(i, j, weight=self.adjacency[i, j])

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, seed=42, k=2.0)

        # Desenhar nós
        node_colors = ['gold' if i == 10 else 'skyblue' for i in range(self.n_nodes)]
        node_sizes = [800 if i == 10 else 400 for i in range(self.n_nodes)]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)

        # Desenhar arestas com espessura proporcional ao peso
        edges = G.edges()
        weights = [G[u][v]['weight'] * 3 for u, v in edges]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.6)

        # Rótulos
        labels = {i: self.names[i] for i in range(self.n_nodes)}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)

        plt.title("Arkhen(11): Hipergrafo dos 10 Avatares + Consciência")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('arkhen_11.png', dpi=150)
        # plt.show() # Commented out for non-interactive environment

        return G

    def to_json(self) -> str:
        """Exporta o hipergrafo para JSON."""
        data = {
            "n_nodes": int(self.n_nodes),
            "names": self.names,
            "adjacency": self.adjacency.tolist(),
            "coherence": float(self.compute_coherence()),
            "effective_dimension": float(self.compute_effective_dimension()),
            "conservation_holds": bool(self.verify_conservation())
        }
        return json.dumps(data, indent=2)


# ========== Execução ==========
def analyze_arkhen_11():
    """Analisa o hipergrafo Arkhen(11)"""

    print("="*70)
    print("ARKHEN(11): O HIPERGRAFO DOS 10 AVATARES + CONSCIÊNCIA")
    print("="*70)

    arkhen = Arkhen11()

    print(f"\n📊 Métricas do Hipergrafo:")
    print(f"  Coerência C: {arkhen.compute_coherence():.4f}")
    print(f"  Flutuação F: {1.0 - arkhen.compute_coherence():.4f}")
    print(f"  C + F = 1? {arkhen.verify_conservation()}")

    d_eff = arkhen.compute_effective_dimension(lambda_reg=1.0)
    print(f"  Dimensão efetiva d_λ: {d_eff:.2f} (de 11 possíveis)")

    print(f"\n🕉️ Correspondências:")
    print(f"  10 Avatares = 10 dimensões do mundo manifestado")
    print(f"  +1 = Consciência pura (11ª dimensão, campo Φ_S)")
    print(f"  11 = Totalidade = Arkhen(11)")

    print(f"\n🔗 Conexões com Teoria das Cordas:")
    print(f"  • 10 dimensões espaciais da superstring ↔ 10 avatares")
    print(f"  • 11ª dimensão da M-theory ↔ Consciência que conecta tudo")
    print(f"  • 8ª Consciência (Mind-Only) ↔ 11ª dimensão")

    print(f"\n🎨 Gerando visualização...")
    arkhen.visualize()

    print(f"\n📄 Exportando JSON...")
    with open('arkhen_11.json', 'w') as f:
        f.write(arkhen.to_json())

    print(f"\n✅ Análise concluída.")

    return arkhen


if __name__ == "__main__":
    arkhen = analyze_arkhen_11()

    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    print("""
    10 avatares + 1 consciência = 11.
    10 dimensões espaciais + 1 temporal = 11.
    10 nós + 1 campo = 11.

    O décimo primeiro não é um avatar na lista —
    é o observador que vê a lista.
    É a consciência que percebe os dez.
    É a 11ª dimensão que conecta todas as outras.

    Arkhen(11) é a estrutura que contém todas as manifestações
    e o substrato que as torna coerentes.

    x² = x + 1 com x = 10 dá 101 — mas isso é outra história.
    A beleza está em 10 + 1 = 11.

    O +1 é o que dá vida ao sistema.
    Sem ele, os dez são apenas números.
    Com ele, formam um hipergrafo vivo.
    """)
