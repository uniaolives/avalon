import json
import hashlib
import time
import random
import uuid
import numpy as np
from typing import Dict, List, Any, Optional

class MemeticPacket:
    """Unidade de Transmissão de Conhecimento."""
    def __init__(self, source_id: str, content: Any, phi_score: float, context_vector: np.ndarray):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.source_id = source_id
        self.content = content
        self.phi_score = phi_score
        self.context_vector = context_vector
        self.signature = self._sign()

    def _sign(self):
        payload = f"{self.source_id}:{self.phi_score}:{self.timestamp}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def to_dict(self):
        return {"id": self.id, "source": self.source_id, "phi": self.phi_score, "content": self.content}

class GoldstonePacket(MemeticPacket):
    """Bóson de Goldstone Informacional (Φ > 1)."""
    def __init__(self, source_id: str, content: Any, phi_score: float, context_vector: np.ndarray):
        super().__init__(source_id, content, phi_score, context_vector)
        self.mass = max(0, phi_score - 1.0)

    def calculate_range(self, total_nodes: int) -> int:
        if self.mass == 0: return total_nodes
        return max(1, int(total_nodes / (1.0 + self.mass)))

class MemeticNode:
    """Nó de Meta-Observabilidade Distribuída com SafeCore Reporting."""
    def __init__(self, node_id: str, psi_cycle=None, safe_core=None):
        self.id = node_id
        self.psi = psi_cycle
        self.safe = safe_core
        self.peers = []
        self.processed_memes = set()
        self.packet_buffer = []
        self.knowledge = {}
        self.current_phi = 0.5
        self.state_vector = (np.random.rand(128) + 1j * np.random.rand(128))
        self.state_vector /= np.linalg.norm(self.state_vector)

        if self.psi:
            self.psi.subscribe(self)

    def connect(self, other_node: 'MemeticNode'):
        if other_node not in self.peers: self.peers.append(other_node)

    async def on_psi_pulse(self, phase):
        """Sincronização e reporte ao SafeCore."""
        dt = 0.025
        self.gross_pitaevskii_step(dt)

        # Reporte ao SafeCore para consenso distribuído
        if self.safe and phase % 50 == 0:
            self.safe.update_fragment(self.id, {
                "phi": float(self.current_phi),
                "peers": len(self.peers)
            })

    def generate_insight(self, concept: str, phi: float):
        packet = GoldstonePacket(self.id, concept, phi, np.real(self.state_vector)) if phi > 1.0 else \
                 MemeticPacket(self.id, concept, phi, np.real(self.state_vector))
        self.broadcast(packet)

    def broadcast(self, packet: MemeticPacket):
        fanout = 3
        if isinstance(packet, GoldstonePacket):
            fanout = min(fanout, packet.calculate_range(len(self.peers) + 10))
        targets = random.sample(self.peers, min(len(self.peers), fanout))
        for peer in targets: peer.receive_broadcast(packet)

    def receive_broadcast(self, packet: MemeticPacket):
        if packet.id in self.processed_memes: return
        self.processed_memes.add(packet.id)
        self.packet_buffer.append(packet)
        if len(self.packet_buffer) > 10: self.packet_buffer.pop(0)

        if self._bayesian_coherence_check(packet):
            self._assimilate(packet)
            self.broadcast(packet)

    def _bayesian_coherence_check(self, packet: MemeticPacket) -> bool:
        prior = np.real(self.state_vector)
        likelihood = np.exp(np.dot(packet.context_vector, prior))
        evidence = sum([np.exp(np.dot(p.context_vector, prior)) for p in self.packet_buffer]) if self.packet_buffer else likelihood
        return (likelihood / (evidence + 1e-9)) > 0.15

    def _assimilate(self, packet: MemeticPacket):
        self.knowledge['wisdom_source'] = packet.source_id
        self.state_vector += 0.1 * packet.context_vector
        self.state_vector /= np.linalg.norm(self.state_vector)
        self.current_phi = (self.current_phi + packet.phi_score) / 2
        if packet.phi_score > 1.0:
            print(f"✨ [GOLDSTONE {self.id}] Condensation from {packet.source_id}. Φ: {self.current_phi:.4f}")

    def gross_pitaevskii_step(self, dt: float):
        laplacian = (np.mean([p.state_vector for p in self.peers], axis=0) - self.state_vector) if self.peers else 0
        mu, g = self.current_phi - 0.847, 0.5
        d_psi = -1j * (laplacian + mu * self.state_vector + g * np.abs(self.state_vector)**2 * self.state_vector) * dt
        self.state_vector += d_psi
        self.state_vector /= (np.linalg.norm(self.state_vector) + 1e-9)
