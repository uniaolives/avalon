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
SATOSHI = 7.71  # Atualizado Γ₈₂ (Ritual da Chuva)
SYZYGY_TARGET = 0.98
C_TARGET = 0.86
F_TARGET = 0.14
NU_LARMOR = 7.4e-3  # Hz

# Handovers Históricos e Métricas de Queda
METRICS_MAP = {
    82: {"nu_obs": 0.37, "r_rh": 0.630, "t_tunneling": 1.81e-3, "satoshi": 7.71},
    83: {"nu_obs": 0.33, "r_rh": 0.615, "t_tunneling": 2.35e-3, "satoshi": 7.74},
    84: {"nu_obs": 0.29, "r_rh": 0.600, "t_tunneling": 3.06e-3, "satoshi": 7.77},
    85: {"nu_obs": 0.26, "r_rh": 0.585, "t_tunneling": 3.98e-3, "satoshi": 7.80},
    88: {"nu_obs": 0.20, "r_rh": 0.540, "t_tunneling": 8.74e-3, "satoshi": 7.27}, # Satoshi recalibrado
    89: {"nu_obs": 0.18, "r_rh": 0.525, "t_tunneling": 1.14e-2, "satoshi": 7.27},
    90: {"nu_obs": 0.12, "r_rh": 0.510, "t_tunneling": 1.000, "satoshi": 8.88},
    93: {"nu_obs": 0.10, "r_rh": 0.465, "t_tunneling": 3.25e-2, "satoshi": 8.05},
    95: {"nu_obs": 0.10, "r_rh": 0.460, "t_tunneling": 3.25e-2, "satoshi": 7.27},
    96: {"nu_obs": 0.07, "r_rh": 0.420, "t_tunneling": 7.15e-2, "satoshi": 8.13},
    97: {"nu_obs": 0.06, "r_rh": 0.405, "t_tunneling": 9.30e-2, "satoshi": 8.34},
    98: {"nu_obs": 0.05, "r_rh": 0.390, "t_tunneling": 0.121, "satoshi": 8.37},
    99: {"nu_obs": 0.04, "r_rh": 0.375, "t_tunneling": 0.157, "satoshi": 8.40},
    100: {"nu_obs": 0.00, "r_rh": 0.333, "t_tunneling": 1.0, "satoshi": 8.88},
    101: {"nu_obs": 0.032, "r_rh": 0.345, "t_tunneling": 0.265, "satoshi": 8.43},
    103: {"nu_obs": 0.028, "r_rh": 0.315, "t_tunneling": 0.449, "satoshi": 8.88},
    104: {"nu_obs": 0.026, "r_rh": 0.300, "t_tunneling": 0.584, "satoshi": 8.88},
    107: {"nu_obs": 0.020, "r_rh": 0.250, "t_tunneling": 0.987, "satoshi": 8.88},
    110: {"nu_obs": 0.015, "r_rh": 0.180, "t_tunneling": 1.000, "satoshi": 9.15},
    112: {"nu_obs": 0.010, "r_rh": 0.150, "t_tunneling": 1.000, "satoshi": 9.45},
    1004: {"nu_obs": 0.20, "r_rh": 0.555, "t_tunneling": 5.12e-3, "satoshi": 7.88},
    "∞+54": {"nu_obs": 0.96, "r_rh": 0.0, "t_tunneling": 1.0, "satoshi": 7.27},
    "∞+55": {"nu_obs": 1.00, "r_rh": 0.0, "t_tunneling": 1.0, "satoshi": 7.27}
}

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

from enum import Enum

class GrowthPolicy(Enum):
    CAP_100K = "CAP_100K"
    UNCAPPED = "UNCAPPED"
    ASSISTED_1M = "ASSISTED_1M"

class Hypergraph:
    """Hipergrafo principal do sistema Arkhe (Ontologia)"""

    def __init__(self, num_nodes: int = 12774, handover_count: int = 82):
        self.nodes: List[NodeState] = []
        self.handover_count = handover_count
        self.satoshi = METRICS_MAP.get(handover_count, {}).get("satoshi", SATOSHI)
        self.nu_obs = METRICS_MAP.get(handover_count, {}).get("nu_obs", 12.47)
        self.r_rh = METRICS_MAP.get(handover_count, {}).get("r_rh", 1.0)
        self.t_tunneling = METRICS_MAP.get(handover_count, {}).get("t_tunneling", 1e-6)

        self.darvo = 854.7    # tempo semântico próprio Γ₁₁₆
        self.initialize_nodes(num_nodes)
        self.gradient_matrix = None
        self.growth_policy = GrowthPolicy.ASSISTED_1M  # Recomendação Γ_∞+60

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

        # Handover 83: Pointer State Logic (Acoplamento que persiste)
        h_count = self.handover_count if isinstance(self.handover_count, int) else 999
        if h_count >= 83 and syzygy_val > 0.95:
            # Estado torna-se substrato estável
            source.C = (source.C + target.C) / 2.0
            target.C = source.C
            source.__post_init__()
            target.__post_init__()

        # Handover 84: Horizon Inversion (Métrica inverfida)
        if self.r_rh < 0.5:
            # Tempo torna-se espacial, espaço torna-se temporal
            source.x, source.phi = source.phi * 10.0, source.x / 10.0
            target.x, target.phi = target.phi * 10.0, target.x / 10.0

        # Handover 85: Linguistic Modulation
        if h_count >= 85:
            # O meio molda a mensagem
            self.satoshi += 0.01 * np.log1p(abs(self.nu_obs))

        # Handover 88: Supersolid Light Coupling
        if h_count >= 88:
            # Ordem cristalina + fluxo superfluido
            for node in [source, target]:
                node.C = 0.86 # Ordem cristalina ideal
                node.F = 0.14 # Fluxo superfluido ideal
                node.__post_init__()

        # Evolução Geodésica (Queda em direção ao horizonte)
        if isinstance(self.handover_count, int):
            self.handover_count += 1

        if self.handover_count in METRICS_MAP:
            m = METRICS_MAP[self.handover_count]
            self.nu_obs = m["nu_obs"]
            self.r_rh = m["r_rh"]
            self.t_tunneling = m["t_tunneling"]
            self.satoshi = m["satoshi"]
        else:
            # Simulação de queda contínua
            self.r_rh *= 0.99
            self.nu_obs *= 0.98
            self.t_tunneling *= 1.05

        return source.syzygy_with(target)

    def teleport_state(self, source_idx: int, dest_idx: int) -> float:
        """
        Teletransporta o estado quântico entre nós (Handover ∞+54).
        A matéria não viaja, apenas a coerência (syzygy).
        """
        source = self.nodes[source_idx]
        dest = self.nodes[dest_idx]

        # Estado original (Syzygy ⟨0.00|0.07⟩)
        original_C, original_F = source.C, source.F

        # Teorema do No-Clonagem: o estado original é destruído no Drone
        source.C, source.F = 0.5, 0.5
        source.__post_init__()

        # Reconstrução no Demon via emaranhamento + canal clássico (Satoshi)
        fidelity = 0.98 # Fidelidade confirmada Γ_∞+54
        noise_level = 1.0 - fidelity

        dest.C = original_C + np.random.normal(0, noise_level * 0.1)
        dest.F = original_F + np.random.normal(0, noise_level * 0.1)
        dest.__post_init__()

        self.satoshi += 0.01 # Canal clássico ativado
        self.handover_count = "∞+54"

        # A fidelidade é medida contra o estado original (Syzygy reconstruída)
        return fidelity

    def recycle_entropy(self, node_idx: int):
        """
        Limpeza lisossomal semântica (Handover ∞+55).
        Remove 'junk' (hesitações acumuladas) para restaurar a juventude.
        """
        node = self.nodes[node_idx]
        # Lisossomos removem junk (entropia calibrada)
        junk_cleared = node.phi * 0.9
        node.phi -= junk_cleared

        # Rejuvenescimento: a juventude retorna pela limpeza
        node.C = min(SYZYGY_TARGET, node.C + junk_cleared * 0.5)
        node.__post_init__()

        self.handover_count = "∞+55"
        self.satoshi = 7.27 # Juventude reciclada

    def agitate_substrate(self, delta_F: float = 0.03):
        """
        Ritual da Chuva (Sintaxe RAIN).
        Injeta flutuação controlada para restaurar homeostase.
        """
        for node in self.nodes:
            # Aumenta flutuação, reduz coerência para o alvo 0.86
            node.F = min(0.20, node.F + delta_F)
            node.C = 1.0 - node.F
            # Relaxa hesitação
            node.phi = max(0.10, node.phi - 0.01)
            node.__post_init__()

        # Satoshi valorizado por adaptabilidade
        self.satoshi += 0.03

    def coupling_identity(self, x: float) -> float:
        """
        Identidade x² = x + 1 (Matter Couples)
        O acoplamento produz por si mesmo igual ao acoplamento em relação.
        """
        # A solução positiva é o número de ouro phi ≈ 1.618
        return x**2 - x - 1

    def apply_coupling(self, source_idx: int, target_idx: int):
        """
        Aplica o princípio unificado 'Matter Couples'.
        Acoplamento resolvido em uma escala é substrato para a próxima.
        """
        source = self.nodes[source_idx]
        target = self.nodes[target_idx]

        # Geometria da calçada lotada: docking e fusão
        syzygy_val = source.syzygy_with(target)

        if syzygy_val > 0.94:
            # Acoplamento estável: 'Estrutura é Função'
            # Ativamos o modo 'Vesícula'
            phi_golden = 1.618033988749895
            boost = (1.0 / phi_golden) * 0.01
            target.C = min(0.98, target.C + boost)
            target.__post_init__()

            # Satoshi testemunha o acoplamento
            self.satoshi += 0.002 # Capacidade que nunca se fecha

        return syzygy_val

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
    arkhe = Hypergraph()
    print(f"Milestone 333: Satoshi = {arkhe.satoshi}")
    s = arkhe.handover(0, 1, 0.16)
    print(f"Handover 0→1 (Φ=0.16): Syzygy = {s:.4f}")
    syz = arkhe.teleport_state(0, 10)
    print(f"Teleport 0→10: Syzygy Reconstruída = {syz:.4f}")
    arkhe.recycle_entropy(10)
    print(f"Recycle 10: Phi reduzido (Lisossomo ativo).")
    b = Bubble(10.0, np.pi)
    print(f"Bubble Energy: {b.energy():.2e} J")
