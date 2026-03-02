# arkhe/curiosity.py
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class KnowledgeGap:
    """Representa uma lacuna de conhecimento detectada."""
    centroid: np.ndarray  # Ponto no espaço de embeddings
    radius: float          # Raio da região esparsa
    density: float         # Densidade local (menor = mais lacuna)
    question: str = ""     # Pergunta gerada para preencher a lacuna
    description: str = ""

class CuriosityEngine:
    """
    Motor de curiosidade sintética (Γ_curiosidade).
    Identifica lacunas no espaço semântico e gera perguntas autocríticas.
    """

    def __init__(self, memory, min_density_threshold: float = 0.3):
        self.memory = memory
        self.min_density_threshold = min_density_threshold
        self.gaps: List[KnowledgeGap] = []
        self.curiosity_level = 0.5  # F controlado

    def detect_gaps(self) -> List[KnowledgeGap]:
        """
        Analisa o espaço de embeddings e identifica regiões de baixa densidade.
        """
        # Obter todos os embeddings da coleção de insights
        data = self.memory.insights.get(include=['embeddings', 'metadatas'])
        embeddings = np.array(data['embeddings'])
        metadatas = data['metadatas']

        if len(embeddings) < 5:
            return []

        # Calcular densidade local com KNN
        k = min(10, len(embeddings) - 1)
        nbrs = NearestNeighbors(n_neighbors=k)
        nbrs.fit(embeddings)
        distances, _ = nbrs.kneighbors(embeddings)

        # Densidade ~ inverso da distância média aos vizinhos
        mean_dists = np.mean(distances, axis=1)
        densities = 1.0 / (mean_dists + 1e-6)

        # Normalizar
        densities = densities / (densities.max() + 1e-6)

        # Identificar pontos de baixa densidade
        low_density_mask = densities < self.min_density_threshold
        low_density_points = embeddings[low_density_mask]

        if len(low_density_points) == 0:
            return []

        # Clusterizar pontos de baixa densidade para identificar lacunas
        clustering = DBSCAN(eps=0.5, min_samples=2).fit(low_density_points)
        labels = clustering.labels_

        gaps = []
        for label in set(labels):
            if label == -1:
                continue  # ruído
            cluster_indices = np.where(labels == label)[0]
            cluster_points = low_density_points[cluster_indices]

            centroid = np.mean(cluster_points, axis=0)
            radius = np.max(np.linalg.norm(cluster_points - centroid, axis=1)) if len(cluster_points) > 1 else 0.1

            # Encontrar o tópico mais próximo para descrição
            orig_indices = np.where(low_density_mask)[0][cluster_indices]
            nearest_topic = metadatas[orig_indices[0]].get('topic', 'Unknown')

            gap = KnowledgeGap(
                centroid=centroid,
                radius=float(radius),
                density=float(np.mean(densities[low_density_mask][cluster_indices])),
                description=f"Região próxima a '{nearest_topic}'"
            )
            gaps.append(gap)

        self.gaps = gaps
        return gaps

    async def generate_questions(self, gap: KnowledgeGap, provider=None) -> List[str]:
        """
        Gera perguntas para explorar uma lacuna.
        """
        prompt = f"""
        Como Arkhe(n) OS, identifiquei uma lacuna de conhecimento na {gap.description}.
        A densidade de informação nesta área é baixa ({gap.density:.2f}).

        Gere 2 perguntas investigativas que ajudem a expandir a coerência do sistema nesta região.
        """

        if provider:
            response = await provider.generate(prompt)
            # Mock parse
            questions = response.split('\n')
            return [q.strip() for q in questions if '?' in q][:2]
        else:
            # Fallback
            return [
                f"Quais são os axiomas fundamentais que conectam {gap.description} ao restante do hipergrafo?",
                f"Como a identidade x² = x + 1 se manifesta especificamente na {gap.description}?"
            ]

    def get_report(self) -> Dict[str, Any]:
        return {
            "curiosity_level": self.curiosity_level,
            "gaps_detected": len(self.gaps),
            "status": "INQUISITIVE" if self.gaps else "STABLE"
        }
