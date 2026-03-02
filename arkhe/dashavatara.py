# arkhe/dashavatara.py
"""
Arkhen(11): Matriz de adjacência do hipergrafo 10+1
Cada avatar é um nó. O décimo primeiro nó é a consciência que os percebe.
(Γ_dashavatara)
"""

import numpy as np
from typing import List, Dict, Any

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
            self.adjacency[i, i+1] = self.adjacency[i+1, i] = max(self.adjacency[i, i+1], 0.3)

    def compute_coherence(self) -> float:
        """
        Calcula a coerência média do sistema.
        """
        # Coerência baseada na densidade de conexões ponderadas
        total_weight = np.sum(self.adjacency) / 2
        max_possible_edges = self.n_nodes * (self.n_nodes - 1) / 2
        return float(total_weight / max_possible_edges)

    def compute_effective_dimension(self, lambda_reg: float = 1.0) -> float:
        """
        Calcula a dimensão efetiva d_λ do hipergrafo.
        d_λ = Σ λ_i/(λ_i+λ) onde λ_i são os autovalores.
        """
        eigenvalues = np.linalg.eigvalsh(self.adjacency)
        # Usar apenas autovalores significativos (positivos)
        pos_eigs = eigenvalues[eigenvalues > 1e-10]
        contributions = pos_eigs / (pos_eigs + lambda_reg)
        return float(np.sum(contributions))

    def verify_conservation(self, tolerance: float = 1e-10) -> bool:
        """Verifica se C + F = 1 se mantém."""
        C = self.compute_coherence()
        F = 1.0 - C
        return abs(C + F - 1.0) < tolerance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_nodes": self.n_nodes,
            "names": self.names,
            "coherence": self.compute_coherence(),
            "effective_dimension": self.compute_effective_dimension(),
            "conservation_holds": self.verify_conservation()
        }
