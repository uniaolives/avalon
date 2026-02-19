import json
import hashlib
import time
import random
import uuid
import numpy as np
from typing import Dict, List, Any, Optional

class MemeticPacket:
    """
    Unidade de Transmissão de Conhecimento Arkhe(N).
    Representa um 'Delta de Sabedoria' propagado pela rede.
    """
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
        return {
            "id": self.id,
            "source": self.source_id,
            "phi": self.phi_score,
            "content": self.content,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

class MemeticNode:
    """
    Nó de Meta-Observabilidade Distribuída.
    Implementa o protocolo de Gossip para propagação de coerência e insights.
    """
    def __init__(self, node_id: str, psi_cycle=None):
        self.id = node_id
        self.psi = psi_cycle
        self.peers = []
        self.processed_memes = set()
        self.knowledge = {}
        self.current_phi = 0.5
        self.state_vector = np.random.rand(128)

        if self.psi:
            self.psi.subscribe(self)

    def connect(self, other_node: 'MemeticNode'):
        if other_node not in self.peers:
            self.peers.append(other_node)

    async def on_psi_pulse(self, phase):
        """Sincronização memética no pulso Ψ."""
        # A cada 100 fases, tenta um 'broadcast de estado' se a coerência for alta
        if phase % 100 == 0 and self.current_phi > 0.8:
            self.generate_insight(f"Coherence State Sync from {self.id}", self.current_phi)

    def generate_insight(self, concept: str, phi: float):
        """Gera e propaga um novo insight memético."""
        packet = MemeticPacket(self.id, concept, phi, self.state_vector)
        self.broadcast(packet)

    def broadcast(self, packet: MemeticPacket):
        """Propagação via Gossip (Epidêmica)."""
        fanout = 3
        targets = random.sample(self.peers, min(len(self.peers), fanout))
        for peer in targets:
            peer.receive_broadcast(packet)

    def receive_broadcast(self, packet: MemeticPacket):
        """Recebe e decide se deve assimilar e retransmitir."""
        if packet.id in self.processed_memes:
            return

        self.processed_memes.add(packet.id)

        # Cálculo de Ressonância
        phi_gain = packet.phi_score - self.current_phi
        resonance = np.clip(0.5 + (phi_gain * 2.0), 0, 1)

        if resonance > 0.7:
            self._assimilate(packet)
            self.broadcast(packet)

    def _assimilate(self, packet: MemeticPacket):
        """Assimilação de conhecimento e evolução do vetor de estado."""
        self.knowledge['wisdom_source'] = packet.source_id
        self.knowledge['latest_content'] = packet.content

        # Evolução do estado (Learning rate adaptativa)
        lr = 0.1
        self.state_vector += lr * (packet.context_vector - self.state_vector)
        self.state_vector /= (np.linalg.norm(self.state_vector) + 1e-9)

        # Elevação de Coerência/Φ
        self.current_phi = (self.current_phi + packet.phi_score) / 2
        print(f"✨ [MEMETIC {self.id}] Assimilated knowledge from {packet.source_id}. New Φ: {self.current_phi:.4f}")
