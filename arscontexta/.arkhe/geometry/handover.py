import numpy as np
from typing import Dict

class FeatureGeometryHandover:
    """
    Handover bidirecional entre representação discreta (features)
    e contínua (manifold) — isomorfo ao handover quântico-clássico.
    """

    def __init__(self, manifold):
        self.feature_dict = {}      # Sparse autoencoder
        self.manifold = manifold    # Instância de CharacterCountManifold
        self.crosscoder = None      # Ponte entre os mundos

    def discrete_to_continuous(self, features: Dict[str, float]) -> np.ndarray:
        """
        Converte ativações discretas (e.g., "count_35_45")
        para ponto no manifold contínuo.
        """
        # Soma ponderada de vetores de base
        point = np.zeros(self.manifold.dim)
        for feat_name, activation in features.items():
            if "count" in feat_name:
                # Extrair valor numérico do nome da feature
                count_val = self._parse_count_range(feat_name)
                point += activation * self.manifold.embed(count_val)

        # Normalizar para ficar na curva
        return self._project_to_manifold(point)

    def continuous_to_discrete(self, point: np.ndarray) -> Dict[str, float]:
        """
        Amostra ponto no manifold para ativações de features discretas.
        """
        # Encontrar feature mais próxima
        nearest_features = {}

        # Decompor em ativações de "place cells" (células de lugar)
        for count in range(0, 150, 5):  # Range de contagem
            feature_vec = self.manifold.embed(count)
            norm_p = np.linalg.norm(point)
            norm_f = np.linalg.norm(feature_vec)

            if norm_p < 1e-10 or norm_f < 1e-10:
                similarity = 0.0
            else:
                similarity = np.dot(point, feature_vec) / (norm_p * norm_f)

            if similarity > 0.5:  # Threshold de ativação
                nearest_features[f"count_{count}_{count+5}"] = similarity

        return nearest_features

    def handover(self, mode: str, state):
        """
        Handover controlado entre modos de representação.
        """
        if mode == "discrete_to_continuous":
            return self.discrete_to_continuous(state)
        elif mode == "continuous_to_discrete":
            return self.continuous_to_discrete(state)
        else:
            raise ValueError(f"Unknown handover mode: {mode}")

    def _parse_count_range(self, feat_name: str) -> int:
        """Extrai o valor médio da contagem a partir do nome da feature."""
        # Formato esperado: count_X_Y
        try:
            parts = feat_name.split("_")
            low = int(parts[1])
            high = int(parts[2])
            return (low + high) // 2
        except:
            return 0

    def _project_to_manifold(self, point: np.ndarray) -> np.ndarray:
        """Projeta um ponto de volta para o manifold (simplificado)."""
        # Em uma implementação real, isso seria uma busca pelo ponto mais próximo na curva
        norm = np.linalg.norm(point)
        if norm < 1e-10:
            return point
        return point # Placeholder
