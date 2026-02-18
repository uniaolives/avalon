import numpy as np

class CharacterCountManifold:
    """
    Implementação do manifold de contagem de caracteres (Gurnee et al.)
    como instância do piloto Arkhe(N) em espaço contínuo.
    """

    def __init__(self, dimension=6):
        self.dim = dimension          # Subespaco de 6 dimensões (95% variância)
        self.curve = None           # Estrutura helicoidal
        self.ring_frequency = 0.1    # Frequência do "ringing" (sinc) - Valor simulado

    def embed(self, count: int) -> np.ndarray:
        """
        Embed contagem escalar em ponto no manifold.

        Ao invés de one-hot (ineficiente) ou escalar (ruído),
        usa espiral: count → (r·cos(θ), r·sin(θ), z...) em 6D
        """
        # Estrutura helicoidal: radius cresce, ângulo acumula
        theta = count * self.ring_frequency
        radius = np.log1p(count)  # Compressão logarítmica

        # Coordenadas no subespaço 6D (simplificado para 3D visualização)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = count / 50.0  # Normalização pela largura da linha

        # Preencher com zeros até a dimensão desejada
        vector = np.zeros(self.dim)
        vector[0] = x
        vector[1] = y
        vector[2] = z

        return vector

    def rotate_to_boundary(self, current: np.ndarray, limit: int) -> float:
        """
        Comparação via rotação (QK circuit).

        Ao invés de subtração (current - limit), rotaciona o manifold
        até que current_count alinhe com limit_vector.

        Retorna: score de atenção (quanto mais alinhado, mais próximo do limite)
        """
        # Criar vetor alvo para o limite
        target = self.embed(limit)

        # Matriz de rotação W_QK "twista" o espaço
        rotation = self._compute_qk_rotation()

        # Aplicar rotação
        rotated_current = rotation @ current

        # Similaridade de cosseno = alinhamento após rotação
        norm_rotated = np.linalg.norm(rotated_current)
        norm_target = np.linalg.norm(target)

        if norm_rotated < 1e-10 or norm_target < 1e-10:
            return 0.0

        alignment = np.dot(rotated_current, target) / (norm_rotated * norm_target)

        return alignment  # Pico quando current ≈ limit - ε

    def _compute_qk_rotation(self) -> np.ndarray:
        """
        A matriz W_QK aprendida pelo modelo efetivamente
        implementa uma transformação que mapeia contagem
        para "distância até o limite" via rotação.
        """
        # Simulação: rotação que alinha eixo z com direção do limite
        # Na prática, é aprendida via atenção durante treinamento
        return np.eye(self.dim)  # Placeholder
