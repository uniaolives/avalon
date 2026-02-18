# papercoder_kernel/core/quantum_pilot/governance.py
"""
Quantum Governance for Autonomous Systems.
Implements Φ (IIT 4.0), Coherence monitoring, and Topological Kill Switch.
Also includes Bidirectional Handover protocols.
"""

import numpy as np
import time
from typing import Dict, Optional
from .pilot_core import QuantumPilotCore

class QuantumGovernanceCore:
    """
    Controlador de Governança Arkhe(N).
    Garante que o piloto opere dentro dos limites éticos e de segurança.
    """
    def __init__(self, phi_threshold: float = 0.1, coherence_threshold: float = 0.5):
        self.phi_threshold = phi_threshold
        self.coherence_threshold = coherence_threshold

    def monitor(self, pilot: QuantumPilotCore) -> Dict:
        """Monitora o piloto em tempo real."""
        # Cálculo de Φ (Phi) - Informação Integrada
        phi = self._calculate_quantum_phi(pilot)
        pilot.phi = phi

        # Verificação de Coerência
        coherence = pilot.coherence

        status = "NOMINAL"
        if phi > self.phi_threshold:
            status = "PHI_CRITICAL"
            self._trigger_kill_switch(pilot, f"Φ {phi:.4f} exceeds threshold {self.phi_threshold}")
        elif coherence < self.coherence_threshold:
            status = "COHERENCE_LOW"
            self._trigger_kill_switch(pilot, f"Coherence {coherence:.4f} below threshold {self.coherence_threshold}")

        return {
            "phi": phi,
            "coherence": coherence,
            "status": status,
            "kill_switch_active": not pilot.active if status != "NOMINAL" else False
        }

    def _calculate_quantum_phi(self, pilot: QuantumPilotCore) -> float:
        """
        Calcula Φ simplificado baseado na entropia de von Neumann.
        Em um sistema quântico real, isso mediria a integração entre subsistemas.
        """
        entanglement_matrix = pilot._quantum_entanglement_matrix()
        # Simulação: Φ é proporcional à norma da matriz de emaranhamento off-diagonal
        off_diag = entanglement_matrix - np.diag(np.diag(entanglement_matrix))
        phi = np.linalg.norm(off_diag) / 100.0 # Normalizado
        return min(phi, 0.2) # Saturado para demonstração

    def _trigger_kill_switch(self, pilot: QuantumPilotCore, reason: str):
        """Desativa o sistema imediatamente (Kill Switch Topológico)."""
        print(f"[GOVERNANCE] KILL SWITCH TRIGGERED: {reason}")
        pilot.stc_array.shutdown()
        pilot.deactivate()

class BidirectionalHandover:
    """
    Handover quântico-clássico bidirecional.
    Permite transferência de controle sem perda de estado.
    """
    def handover_to_classical(self, quantum_pilot: QuantumPilotCore, classical_ctrl: Dict) -> Dict:
        print("[HANDOVER] Transferring to Classical Supervision...")
        # Salva o estado atual da política quântica
        policy = quantum_pilot.nav_q.extract_policy()
        classical_ctrl["imported_policy"] = policy
        quantum_pilot.deactivate()
        return {"status": "CLASSICAL_MODE", "policy_integrated": True}

    def handover_to_quantum(self, classical_ctrl: Dict, quantum_pilot: QuantumPilotCore) -> Dict:
        print("[HANDOVER] Reinstating Quantum Autonomy...")
        quantum_pilot.activate()
        return {"status": "QUANTUM_MODE", "coherence_restored": True}

class QuantumHandoverProtocol:
    """Protocolo de transferência de estado entre nós móveis."""
    def execute(self, source_id: str, target_id: str, state: np.ndarray) -> bool:
        print(f"[HANDOVER] Quantum Teleportation: {source_id} -> {target_id}")
        # Simula fidelidade de 99%
        fidelity = 0.99
        return fidelity > 0.95
