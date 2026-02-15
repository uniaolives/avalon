# arkhe/qkd.py
"""
Quantum Key Distribution (Γ_qkd)
Integrates QKD for secure communication, leveraging Darvo state for key lifetime.
"""

import secrets
import time
import hashlib
from typing import Dict, Optional

class QKDManager:
    """
    Gerenciador de Distribuição de Chaves Quânticas.
    Protege os canais de comunicação contra ameaças quânticas.
    """
    def __init__(self, initial_darvo: float = 854.7):
        self.active_keys: Dict[str, str] = {}
        self.key_metadata: Dict[str, Dict] = {}
        self.darvo_state = initial_darvo
        self.entropy_pool = secrets.token_bytes(64)

    def update_darvo(self, current_darvo: float):
        """Atualiza o estado temporal semântico do protocolo Darvo."""
        self.darvo_state = current_darvo

    def generate_quantum_key(self, channel_id: str, bits: int = 256) -> str:
        """
        Gera uma chave resistente a quantum baseada em entropia local.
        A vida útil da chave é inversamente proporcional à hesitação capturada pelo Darvo.
        """
        key = secrets.token_hex(bits // 8)

        # Calcular tempo de vida:
        # Base de 3600s ajustada pelo estado Darvo (854.7 como referência)
        # Se darvo aumenta (mais tempo semântico/hesitação), o tempo de vida diminui
        base_lifetime = 3600.0
        adjusted_lifetime = base_lifetime * (854.7 / max(self.darvo_state, 1.0))

        self.active_keys[channel_id] = key
        self.key_metadata[channel_id] = {
            "created_at": time.time(),
            "expires_at": time.time() + adjusted_lifetime,
            "bits": bits,
            "darvo_snapshot": self.darvo_state
        }

        print(f"🔐 [QKD] Chave gerada para canal '{channel_id}'. Vida útil: {adjusted_lifetime:.1f}s")
        return key

    def get_valid_key(self, channel_id: str) -> Optional[str]:
        """Recupera uma chave se ela ainda for válida."""
        if channel_id not in self.active_keys:
            return None

        meta = self.key_metadata[channel_id]
        if time.time() > meta["expires_at"]:
            print(f"⚠️ [QKD] Chave do canal '{channel_id}' expirou (Excedeu horizonte Darvo).")
            del self.active_keys[channel_id]
            del self.key_metadata[channel_id]
            return None

        return self.active_keys[channel_id]

    def sign_message(self, channel_id: str, message: str) -> str:
        """Assina uma mensagem usando a chave QKD ativa."""
        key = self.get_valid_key(channel_id)
        if not key:
            raise ValueError("Nenhuma chave QKD válida disponível para este canal.")

        payload = f"{message}|{key}|{self.darvo_state}"
        return hashlib.sha3_256(payload.encode()).hexdigest()
