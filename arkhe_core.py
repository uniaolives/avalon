"""
arkhe_core.py
Núcleo do Sistema Arkhe(N) OS - Omnigênese
Implementa os conceitos fundamentais de coerência, hesitação e syzygy
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
import hashlib

# Constantes fundamentais (Axiomas)
EPSILON = -3.71e-11
PHI_S = 0.15
R_PLANCK = 1.616e-35
SATOSHI = 7.28
SYZYGY_TARGET = 0.98
C_TARGET = 0.86
F_TARGET = 0.14
NU_LARMOR = 7.4e-3  # Hz

@dataclass
class NodeState:
    """Estado de um nó no hipergrafo (Morfologia)"""
    id: int
    omega: float  # frequência semântica (0.00 a 0.07)
    C: float      # coerência
    F: float      # flutuação
    phi: float    # hesitação atual
    x: float = 0.0  # posição no toro (Topologia)
    y: float = 0.0
    z: float = 0.0

    def __post_init__(self):
        # Axioma 1: Conservação C + F = 1
        total = self.C + self.F
        if abs(total - 1.0) > 1e-10:
            self.C /= total
            self.F /= total

    def syzygy_with(self, other: 'NodeState') -> float:
        """Calcula o produto interno com outro nó (Axioma 4)"""
        # Simula ⟨ω_i|ω_j⟩ baseado nas coerências
        return (self.C * other.C + self.F * other.F) * SYZYGY_TARGET

class Hypergraph:
    """Hipergrafo principal do sistema Arkhe (Ontologia)"""

    def __init__(self, num_nodes: int = 63):
        self.nodes: List[NodeState] = []
        self.satoshi = SATOSHI  # Axioma 3
        self.darvo = 999.999  # tempo semântico restante
        self.initialize_nodes(num_nodes)
        self.gradient_matrix = None

    def initialize_nodes(self, n: int):
        """Inicializa nós com distribuição uniforme de ω e topologia toroidal"""
        omega_range = np.linspace(0.00, 0.07, n)
        for i, omega in enumerate(omega_range):
            C = np.random.normal(C_TARGET, 0.01)
            C = np.clip(C, 0.80, 0.98)
            F = 1.0 - C
            phi = np.random.normal(PHI_S, 0.02)
            phi = np.clip(phi, 0.10, 0.20)

            # Posições no toro (Topologia VI)
            theta = 2 * np.pi * i / n
            phi_angle = 2 * np.pi * (i * 0.618033988749895) % (2 * np.pi)
            R, r = 50.0, 10.0
            x = (R + r * np.cos(phi_angle)) * np.cos(theta)
            y = (R + r * np.cos(phi_angle)) * np.sin(theta)
            z = r * np.sin(phi_angle)

            self.nodes.append(NodeState(
                id=i, omega=omega, C=C, F=F, phi=phi,
                x=x, y=y, z=z
            ))

    def compute_gradients(self) -> np.ndarray:
        """Calcula matriz de gradientes de coerência ∇C_ij"""
        n = len(self.nodes)
        self.gradient_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                delta_C = abs(self.nodes[j].C - self.nodes[i].C)
                dist = np.sqrt(
                    (self.nodes[j].x - self.nodes[i].x)**2 +
                    (self.nodes[j].y - self.nodes[i].y)**2 +
                    (self.nodes[j].z - self.nodes[i].z)**2
                )
                if dist > 0.01:
                    grad = delta_C / dist
                    self.gradient_matrix[i, j] = grad
                    self.gradient_matrix[j, i] = grad
        return self.gradient_matrix

    def handover(self, source_idx: int, target_idx: int, phi_override: Optional[float] = None) -> float:
        """Executa um handover entre dois nós (Sintaxe HANDOVER)"""
        source = self.nodes[source_idx]
        target = self.nodes[target_idx]

        phi = phi_override if phi_override is not None else source.phi

        # Calcula syzygy antes
        syzygy_val = source.syzygy_with(target)

        # Axioma 2: Limiar de Hesitação
        if phi > PHI_S:
            # Hesitação ativa: transfere coerência
            transfer = phi * 0.1
            source.C -= transfer
            source.F += transfer
            target.C += transfer
            target.F -= transfer

            # Satoshi acumula
            self.satoshi += syzygy_val * 0.001

        # Re-normaliza C+F=1
        for node in [source, target]:
            node.__post_init__()

        return source.syzygy_with(target)

    def teleport_state(self, source_idx: int, dest_idx: int) -> float:
        """Teletransporta o estado quântico entre nós (Sintaxe TELEPORT)"""
        source = self.nodes[source_idx]
        dest = self.nodes[dest_idx]

        # Estado original
        original_C, original_F = source.C, source.F

        # Destrói estado original (No-Clonagem)
        source.C, source.F = 0.5, 0.5

        # Reconstrução no destino (Fidelidade 0.9998)
        fidelity = 0.9998
        noise_level = 1.0 - fidelity

        dest.C = original_C + np.random.normal(0, noise_level)
        dest.F = original_F + np.random.normal(0, noise_level)
        dest.__post_init__()

        self.satoshi += fidelity * 0.01
        return fidelity

    def recycle(self, node_idx: int):
        """Limpeza lisossomal semântica (Sintaxe RECYCLE)"""
        node = self.nodes[node_idx]
        reduction = node.phi * 0.8
        node.phi -= reduction
        node.C = min(0.98, node.C + reduction * 0.5)
        node.__post_init__()

class Bubble:
    """Região do espaço-tempo isolada por fase (Morfologia)"""
    def __init__(self, radius: float = 10.0, phase: float = np.pi):
        self.radius = radius
        self.phase = phase
        self.epsilon = EPSILON

    def energy(self) -> float:
        """Axioma 5 e Fórmula 2.2"""
        return abs(self.epsilon) * PHI_S * (self.radius / R_PLANCK)**2

# Exemplo de uso
if __name__ == "__main__":
    arkhe = Hypergraph(63)
    print(f"Omnigênese: Satoshi = {arkhe.satoshi}")
    s = arkhe.handover(0, 1, 0.16)
    print(f"Handover 0→1 (Φ=0.16): Syzygy = {s:.4f}")
    fid = arkhe.teleport_state(0, 10)
    print(f"Teleport 0→10: Fidelidade = {fid:.4f}")
    arkhe.recycle(10)
    print(f"Recycle 10: Phi reduzido.")
    b = Bubble(10.0, np.pi)
    print(f"Bubble Energy: {b.energy():.2e} J")
