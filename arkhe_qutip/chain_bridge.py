import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import qutip as qt

@dataclass
class HandoverRecord:
    handover_id: str
    node_id: str
    timestamp: float
    chain_tx_hash: str
    chain_block_height: int
    metadata: Dict[str, Any]

class ArkheChainBridge:
    """
    Mock bridge to the Arkhe(N)Chain blockchain.
    Records quantum handover events and simulation results.
    """
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self.chain_height = 1000
        self.local_ledger: List[HandoverRecord] = []

    def record_handover(self, event: Any, node_id: str) -> HandoverRecord:
        """Records a single handover event on the chain."""
        self.chain_height += 1

        # Create a mock transaction hash
        payload = f"{node_id}:{self.chain_height}:{time.time()}"
        tx_hash = hashlib.sha256(payload.encode()).hexdigest()

        record = HandoverRecord(
            handover_id=getattr(event, 'event_id', str(uuid.uuid4())),
            node_id=node_id,
            timestamp=getattr(event, 'timestamp', time.time()),
            chain_tx_hash=tx_hash,
            chain_block_height=self.chain_height,
            metadata=getattr(event, 'metadata', {})
        )

        self.local_ledger.append(record)
        return record

    def record_simulation(self, psi_initial: Any, psi_final: Any,
                          metadata: Optional[Dict[str, Any]] = None) -> HandoverRecord:
        """Records a whole simulation result."""
        self.chain_height += 1

        node_id = getattr(psi_initial, 'node_id', 'unknown_node')
        payload = f"SIM:{node_id}:{self.chain_height}"
        tx_hash = hashlib.sha256(payload.encode()).hexdigest()

        record = HandoverRecord(
            handover_id=str(uuid.uuid4()),
            node_id=node_id,
            timestamp=time.time(),
            chain_tx_hash=tx_hash,
            chain_block_height=self.chain_height,
            metadata=metadata or {}
        )

        self.local_ledger.append(record)
        return record

    def get_node_history(self, node_id: str) -> List[HandoverRecord]:
        """Queries the chain for a specific node's history."""
        return [r for r in self.local_ledger if r.node_id == node_id]
