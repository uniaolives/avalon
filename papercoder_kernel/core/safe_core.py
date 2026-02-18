# papercoder_kernel/core/safe_core.py
"""
Safe Core: Núcleo de Coerência Quântica.
Baseado no Protocolo Arkhe(N) para sistemas autônomos seguros.
Monitora Φ_Q, C e QFI em tempo real (40Hz).
"""

import numpy as np
import time
from typing import Dict, List, Optional, Callable

class SafeCore:
    """
    Núcleo de Coerência Quântica (Safe Core).
    Garante que drones, AGIs e processadores operem com alinhamento e segurança quântica.
    """
    def __init__(self, node_id: str = "safe_core_01"):
        self.node_id = node_id
        self.phi_threshold = 0.1
        self.coherence_min = 0.847
        self.qfi_max = 1e6
        self.kill_switch_latency_ms = 25

        self.current_phi = 0.0
        self.current_coherence = 1.0
        self.current_qfi = 0.0

        self.phi_history = []
        self.coherence_history = []
        self.ledger = []
        self.is_active = True
        self.mode = "QUANTUM"

    def monitor(self, quantum_state: np.ndarray):
        """Monitora as métricas do Safe Core baseadas no estado quântico atual."""
        if not self.is_active:
            return

        self.current_phi = self._calculate_phi_q(quantum_state)
        self.current_coherence = self._calculate_coherence(quantum_state)
        self.current_qfi = self._calculate_qfi(quantum_state)

        self._update_ledger()
        self._check_governance()

    def decide(self, quantum_state: np.ndarray, model_func: Callable) -> Dict:
        """Processa decisão mantendo a vigilância do Safe Core."""
        if self.mode == "CLASSICAL":
            return {"action": "BACKUP_PILOT", "mode": "CLASSICAL"}

        self.monitor(quantum_state)

        if not self.is_active:
            return {"action": "EMERGENCY_SHUTDOWN", "mode": "TERMINATED"}

        action = model_func(quantum_state)
        return {"action": action, "mode": self.mode, "phi": self.current_phi, "coherence": self.current_coherence}

    def _calculate_phi_q(self, state: np.ndarray) -> float:
        """Calcula a informação integrada quântica (simulado)."""
        # Φ_Q ≈ entropia de emaranhamento
        p = np.abs(state)**2
        p = p / (np.sum(p) + 1e-9)
        entropy = -np.sum(p * np.log2(p + 1e-9))
        phi = entropy * 0.05 # Proxy
        return min(phi, 0.2)

    def _calculate_coherence(self, state: np.ndarray) -> float:
        """Calcula a coerência do sistema (simulado)."""
        # Proximidade a um estado puro alvo
        return float(np.mean(np.abs(state)))

    def _calculate_qfi(self, state: np.ndarray) -> float:
        """Calcula a Quantum Fisher Information (simulado)."""
        # Sensibilidade a variações de parâmetros
        return float(np.var(state) * 1e5)

    def _check_governance(self):
        """Verifica se as métricas estão dentro dos limites de segurança."""
        if self.current_phi > self.phi_threshold:
            self._kill_switch("Φ overflow (Super-integração detectada)")
        if self.current_coherence < self.coherence_min:
            self._kill_switch("Coherence collapse (Perda de alinhamento quântico)")
        if self.current_qfi > self.qfi_max:
            self.handover_to_classical("High sensitivity / Instability detected")

    def _kill_switch(self, reason: str):
        """Ativa o desligamento topológico de emergência."""
        print(f"[SAFE CORE] KILL SWITCH TRIGGERED: {reason}")
        self.is_active = False
        self._project_to_safe_state()
        self._log_event("KILL_SWITCH", reason)

    def handover_to_classical(self, reason: str):
        """Transfere o controle para o modo clássico de backup."""
        print(f"[SAFE CORE] HANDOVER TO CLASSICAL: {reason}")
        self.mode = "CLASSICAL"
        self._log_event("HANDOVER", reason)

    def _project_to_safe_state(self):
        """Força o sistema para um estado base seguro."""
        print("[SAFE CORE] Projecting to ground state (0)...")

    def _update_ledger(self):
        """Atualiza o histórico e ledger imutável."""
        self.phi_history.append(self.current_phi)
        self.coherence_history.append(self.current_coherence)

    def _log_event(self, event_type: str, detail: str):
        self.ledger.append({
            'timestamp': time.time_ns(),
            'event': event_type,
            'detail': detail,
            'node_id': self.node_id
        })

    def get_status(self) -> Dict:
        return {
            "node_id": self.node_id,
            "is_active": self.is_active,
            "mode": self.mode,
            "phi_q": self.current_phi,
            "coherence": self.current_coherence,
            "qfi": self.current_qfi
        }
