#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARKHE(N) LANGUAGE (ANL) – Core Python Module
============================================
Implementação unificada dos conceitos fundamentais da ANL.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from enum import Enum
import time
from collections import defaultdict

# ============================================================================
# 1. PRIMITIVAS FUNDAMENTAIS
# ============================================================================

class Protocol(Enum):
    """How a handover preserves or transforms information."""
    CONSERVATIVE = 1   # preserves quantities (energy, coherence)
    CREATIVE = 2       # creates new information or structure (stochastic sampling)
    DESTRUCTIVE = 3    # dissipates or removes (forgetting)
    TRANSMUTATIVE = 4  # changes type (e.g., string → embedding)


@dataclass
class StateSpace:
    """Description of the state space of a node."""
    dimension: int
    topology: str           # "euclidean", "spherical", "hyperbolic", "discrete", etc.
    algebra: str            # "real", "complex", "quaternion", "binary"

    def metric(self, a: np.ndarray, b: np.ndarray) -> float:
        """Default Euclidean metric."""
        return float(np.linalg.norm(a - b))


class Node:
    """Fundamental entity in a hypergraph."""
    def __init__(self, node_id: str, state_space: StateSpace, initial_state: Any,
                 local_coherence: float = 1.0):
        self.id = node_id
        self.state_space = state_space
        self.state = initial_state
        self.local_coherence = local_coherence
        self._internal_dynamics: Optional[Callable] = None
        self._observables: Dict[str, Callable] = {}
        self.history: List[Dict] = []

    def set_dynamics(self, dynamics_func: Callable):
        self._internal_dynamics = dynamics_func

    def evolve(self, dt: float) -> 'Node':
        if self._internal_dynamics:
            self.state = self._internal_dynamics(self.state, dt)
        return self

    def _record_history(self, event: str, **kwargs):
        self.history.append({'timestamp': time.time(), 'event': event, **kwargs})

    def __repr__(self):
        return f"Node(id={self.id}, coherence={self.local_coherence:.3f})"


class Handover:
    """Interaction between nodes."""
    def __init__(self, handover_id: str, source: Node, target: Node,
                 protocol: Protocol = Protocol.CONSERVATIVE):
        self.id = handover_id
        self.source = source
        self.target = target
        self.protocol = protocol
        self._mapping: Optional[Callable] = None
        self.effects: List[Callable] = []

    def set_mapping(self, mapping_func: Callable):
        self._mapping = mapping_func

    def add_effect(self, effect_func: Callable):
        self.effects.append(effect_func)

    def execute(self, context: Dict = None) -> Any:
        if self._mapping:
            self.target.state = self._mapping(self.source.state)
        for effect in self.effects:
            effect(self, context)
        return self.target.state


class Hypergraph:
    """Collection of nodes and handovers."""
    def __init__(self, name: str = "Hypergraph"):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.handovers: Dict[str, Handover] = {}
        self.global_coherence: float = 1.0

    def add_node(self, node: Node) -> 'Hypergraph':
        self.nodes[node.id] = node
        return self

    def add_handover(self, handover: Handover) -> 'Hypergraph':
        self.handovers[handover.id] = handover
        return self

    def evolve(self, dt: float, steps: int = 1):
        """Evolve all nodes in the hypergraph."""
        for _ in range(steps):
            for node in self.nodes.values():
                node.evolve(dt)
        return self

    def compute_integration(self) -> float:
        """Simplified Phi (Information Integration)."""
        states = []
        for node in self.nodes.values():
            if isinstance(node.state, (int, float, np.number)):
                states.append(np.array([node.state], dtype=float))
            elif hasattr(node.state, 'flatten'):
                states.append(node.state.flatten())
        if len(states) < 2: return 0.0
        try:
            X = np.stack(states)
            corr = np.corrcoef(X)
            if np.any(np.isnan(corr)): return 0.0
            off_diag = corr[~np.eye(corr.shape[0], dtype=bool)]
            return float(np.mean(np.abs(off_diag)))
        except: return 0.0

# ============================================================================
# 2. MODELOS AVANÇADOS (AGI / INFERÊNCIA ATIVA)
# ============================================================================

class ActiveInferenceNode(Node):
    """
    Nó que implementa o Princípio da Energia Livre e Aprendizagem de Dirichlet.
    """
    def __init__(self, node_id: str, state_space: StateSpace, n_states: int, n_obs: int):
        # O 'state' aqui representa a crença interna q(s)
        initial_belief = np.ones(n_states) / n_states
        super().__init__(node_id, state_space, initial_belief)

        self.n_states = n_states
        self.n_obs = n_obs

        # Dirichlet counters para a Matriz A (Likelihood)
        self.a_dirichlet = np.ones((n_obs, n_states)) * 0.1

        # Preferências (Matriz C) - default neutro (Curiosidade Pura)
        self.C = np.zeros(n_obs)

    def get_A(self) -> np.ndarray:
        """Calcula a Likelihood normalizando Dirichlet."""
        return self.a_dirichlet / self.a_dirichlet.sum(axis=0, keepdims=True)

    def update_belief(self, observation_idx: int):
        """Inferência Bayesiana: atualiza q(s)."""
        A = self.get_A()
        likelihood = A[observation_idx, :]
        posterior = likelihood * self.state
        self.state = posterior / (posterior.sum() + 1e-16)
        return self.state

    def learn(self, observation_idx: int, learning_rate: float = 1.0):
        """Aprendizagem Online via Dirichlet."""
        self.a_dirichlet[observation_idx, :] += learning_rate * self.state
        return self.get_A()

    def compute_epistemic_G(self, B: np.ndarray) -> np.ndarray:
        """
        Calcula G focando apenas na redução da incerteza (Curiosidade Epistêmica).
        Retorna o valor epistêmico (quanto maior, mais informativo).
        """
        n_actions = B.shape[2]
        A = self.get_A()
        G = np.zeros(n_actions)

        # Entropia da Likelihood (Incerteza sobre o mapeamento estado -> observação)
        H_A = -np.sum(A * np.log(A + 1e-16), axis=0)

        for a in range(n_actions):
            expected_state = B[:, :, a] @ self.state
            # G = Epistemic Value (Incerteza esperada do estado futuro)
            G[a] = np.dot(H_A, expected_state)

        return G

    def compute_G(self, B: np.ndarray) -> np.ndarray:
        """Calcula G completo (Pragmático - Epistêmico) para minimização."""
        n_actions = B.shape[2]
        A = self.get_A()
        G = np.zeros(n_actions)
        H_A = -np.sum(A * np.log(A + 1e-16), axis=0)
        for a in range(n_actions):
            expected_state = B[:, :, a] @ self.state
            expected_obs = A @ expected_state
            pragmatic = -np.sum(expected_obs * self.C)
            epistemic = np.dot(H_A, expected_state)
            G[a] = pragmatic - epistemic
        return G

# ============================================================================
# 3. UTILITÁRIOS
# ============================================================================

def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    p = p / (p.sum() + 1e-16)
    q = q / (q.sum() + 1e-16)
    return float(np.sum(p * np.log((p + 1e-16) / (q + 1e-16))))

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-16))

# Shared Memory e outros mantidos para compatibilidade...
class SharedMemory(Node):
    def __init__(self, node_id: str, storage_type: str = "vector", dim: int = 384):
        super().__init__(node_id, StateSpace(0, "abstract", "real"), {})
        self.data = {}
        self.vectors = {}
    def write(self, key, value, embedding=None):
        self.data[key] = value
        if embedding is not None: self.vectors[key] = embedding
    def query_vector(self, query_emb, top_k=5):
        if not self.vectors: return []
        keys = list(self.vectors.keys())
        embs = np.array([self.vectors[k] for k in keys])
        sim = np.dot(embs, query_emb) / (np.linalg.norm(embs, axis=1) * np.linalg.norm(query_emb) + 1e-8)
        top_idx = np.argsort(sim)[-top_k:][::-1]
        return [(keys[i], self.data[keys[i]]) for i in top_idx if i < len(keys)]

if __name__ == "__main__":
    print("Módulo ANL carregado.")
