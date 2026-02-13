"""
ledger.py
Sistema de ledger imutável para registro de handovers
"""

import hashlib
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class HandoverRecord:
    """Registro de um handover"""
    block: int
    timestamp: float
    source_node: int
    target_node: int
    syzygy_before: float
    syzygy_after: float
    satoshi_delta: float
    phi_source: float
    phi_target: float
    hash_prev: str
    hash_self: str = None

    def __post_init__(self):
        if self.hash_self is None:
            self.hash_self = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calcula hash do bloco"""
        data = f"{self.block}{self.timestamp}{self.source_node}{self.target_node}"
        data += f"{self.syzygy_before}{self.syzygy_after}{self.satoshi_delta}"
        data += f"{self.phi_source}{self.phi_target}{self.hash_prev}"
        return hashlib.sha256(data.encode()).hexdigest()

class ArkheLedger:
    """Ledger imutável do sistema Arkhe"""

    def __init__(self):
        self.blocks: List[HandoverRecord] = []
        self.current_satoshi = 7.28
        self.current_block = 0

    def add_handover(self, source: int, target: int,
                     syzygy_before: float, syzygy_after: float,
                     phi_s: float, phi_t: float) -> HandoverRecord:
        """Adiciona registro de handover ao ledger"""
        delta_satoshi = syzygy_after * 0.001
        self.current_satoshi += delta_satoshi

        prev_hash = self.blocks[-1].hash_self if self.blocks else '0'*64

        record = HandoverRecord(
            block=self.current_block,
            timestamp=time.time(),
            source_node=source,
            target_node=target,
            syzygy_before=syzygy_before,
            syzygy_after=syzygy_after,
            satoshi_delta=delta_satoshi,
            phi_source=phi_s,
            phi_target=phi_t,
            hash_prev=prev_hash
        )

        self.blocks.append(record)
        self.current_block += 1
        return record

    def verify_integrity(self) -> bool:
        """Verifica integridade de toda a cadeia"""
        for i in range(1, len(self.blocks)):
            if self.blocks[i].hash_prev != self.blocks[i-1].hash_self:
                return False
            if self.blocks[i].calculate_hash() != self.blocks[i].hash_self:
                return False
        return True

    def export_json(self, filename: str):
        """Exporta ledger para arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump([asdict(b) for b in self.blocks], f, indent=2)

    def get_satoshi_history(self) -> List[float]:
        """Retorna histórico do Satoshi"""
        satoshi = [7.28]
        for b in self.blocks:
            satoshi.append(satoshi[-1] + b.satoshi_delta)
        return satoshi

if __name__ == "__main__":
    ledger = ArkheLedger()
    for i in range(5):
        ledger.add_handover(0, 1, 0.98, 0.98, 0.15, 0.14)
    print(f"Integridade do ledger: {ledger.verify_integrity()}")
    print(f"Satoshi final: {ledger.current_satoshi:.4f}")
