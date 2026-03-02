# glp_interface.py
import torch
import numpy as np
from typing import List

class GLPModel:
    def __init__(self, model_path: str, input_dim: int, n_meta_neurons: int):
        self.input_dim = input_dim
        self.n_meta_neurons = n_meta_neurons
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Simula carregamento de um modelo GLP pré‑treinado
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, n_meta_neurons)
        ).to(self.device)
        # Carrega pesos (aqui, aleatórios; na prática, carregar checkpoint)
        self.model.eval()

    def encode(self, activations: np.ndarray) -> np.ndarray:
        """Converte ativações brutas em meta‑neurônios (projeção interpretável)"""
        with torch.no_grad():
            x = torch.tensor(activations, dtype=torch.float32).to(self.device)
            meta = self.model(x)
        return meta.cpu().numpy()

    def steer(self, meta: np.ndarray, concept_direction: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """Ajusta as ativações originais para reforçar um conceito"""
        # Método simplificado: adiciona direção do conceito no espaço meta
        meta_steered = meta + strength * concept_direction
        # (Na prática, seria necessário inverter a projeção)
        return meta_steered

    def get_concept_direction(self, concept_name: str) -> np.ndarray:
        """Retorna um vetor direcional associado a um conceito (pré‑definido)"""
        # Aqui, retorna um vetor aleatório; na prática, viria de análise de meta‑neurônios
        return np.random.randn(self.n_meta_neurons)
