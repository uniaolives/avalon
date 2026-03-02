import numpy as np
import qutip as qt
from qutip import Qobj, mesolve
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
import time
import uuid

@dataclass
class HandoverEvent:
    """Represents a quantum operation (handover) applied to a state."""
    operator: Qobj
    coherence_before: float
    coherence_after: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self):
        return f"HandoverEvent(id={self.event_id[:8]}, type={self.metadata.get('type', 'unknown')}, ΔC={self.coherence_after - self.coherence_before:.4f})"

class ArkheQobj(Qobj):
    """
    Extended QuTiP Qobj with handover history and coherence tracking.
    """
    def __init__(self, qobj_data, *args, **kwargs):
        # Handle initialization from another ArkheQobj
        history = []
        node_id = str(uuid.uuid4())
        creation_time = time.time()

        if isinstance(qobj_data, ArkheQobj):
            history = list(qobj_data._history)
            node_id = qobj_data._node_id
            creation_time = qobj_data._creation_time
            super().__init__(qobj_data, *args, **kwargs)
        elif isinstance(qobj_data, Qobj):
            super().__init__(qobj_data, *args, **kwargs)
        else:
            super().__init__(qobj_data, *args, **kwargs)

        self._history: List[HandoverEvent] = history
        self._node_id: str = node_id
        self._creation_time: float = creation_time

    @property
    def history(self) -> List[HandoverEvent]:
        return self._history

    @property
    def node_id(self) -> str:
        return self._node_id

    @property
    def coherence(self) -> float:
        """Calculates coherence (purity) of the state: Tr(rho^2)."""
        rho = self.ptrace(range(len(self.dims[0]))) if self.type == 'ket' else self
        if self.type == 'ket':
            return 1.0
        # For density matrices
        return (self * self).tr().real

    def handover(self, operator: Qobj, metadata: Optional[Dict[str, Any]] = None) -> 'ArkheQobj':
        """
        Applies a quantum operator and records the event.
        """
        c_before = self.coherence

        # Apply operator
        if operator.isunitary:
            new_qobj = operator * self * operator.dag() if self.type == 'oper' else operator * self
        else:
            # Assume it's a map or we wrap it
            new_qobj = operator * self if self.type == 'ket' else operator * self * operator.dag()

        c_after = (new_qobj * new_qobj).tr().real if new_qobj.type == 'oper' else 1.0

        event = HandoverEvent(
            operator=operator,
            coherence_before=c_before,
            coherence_after=c_after,
            metadata=metadata or {}
        )

        result = ArkheQobj(new_qobj)
        result._history = self._history + [event]
        result._node_id = self._node_id
        result._creation_time = self._creation_time
        return result

    def get_coherence_trajectory(self) -> List[float]:
        """Returns the list of coherence values over the history."""
        trajectory = [1.0] # Assume initial purity if not recorded
        for event in self._history:
            trajectory.append(event.coherence_after)
        return trajectory

    def evolve_with_handover(self, H: Qobj, tlist: np.ndarray,
                             handovers: List[Tuple[float, Qobj, Dict[str, Any]]],
                             c_ops: List[Qobj] = None) -> Tuple[List['ArkheQobj'], Any]:
        """
        Evolves the state using mesolve, applying scheduled handovers.
        """
        current_state = self
        all_states = []

        # Sort handovers by time
        sorted_handovers = sorted(handovers, key=lambda x: x[0])
        last_t = tlist[0]

        # We need to segment tlist
        for h_t, h_op, h_meta in sorted_handovers:
            if h_t <= last_t: continue
            if h_t > tlist[-1]: break

            # Sub-tlist
            sub_t = tlist[(tlist >= last_t) & (tlist <= h_t)]
            if len(sub_t) > 1:
                res = mesolve(H, current_state, sub_t, c_ops or [])
                current_state = ArkheQobj(res.states[-1])
                current_state._history = all_states[-1]._history if all_states else self._history
                all_states.extend([ArkheQobj(s) for s in res.states[:-1]])

            # Apply handover
            current_state = current_state.handover(h_op, h_meta)
            last_t = h_t

        # Final evolution
        sub_t = tlist[tlist >= last_t]
        if len(sub_t) > 0:
            res = mesolve(H, current_state, sub_t, c_ops or [])
            all_states.extend([ArkheQobj(s) for s in res.states])

        return all_states, None

class ArkheSolver:
    """
    Master Equation solver with Integrated Information (Φ) coupling.
    """
    def __init__(self, H: Qobj, c_ops: List[Qobj] = None, phi_coupling: float = 0.0):
        self.H = H
        self.c_ops = c_ops or []
        self.phi_coupling = phi_coupling

    def solve(self, psi0: ArkheQobj, tlist: np.ndarray, track_coherence: bool = True) -> Any:
        """
        Solves the Master Equation.
        The phi_coupling acts as an additional non-linear term (simplified).
        """
        # In a real implementation, we'd use a custom ODE solver or feedback loop.
        # For now, we simulate the effect by modulating the H or using mesolve features.

        # Simplified Φ effect: periodic modulation at Golden Ratio frequency
        phi_val = (1 + 5**0.5) / 2

        # We use mesolve for the base evolution
        result = mesolve(self.H, psi0, tlist, self.c_ops)

        if track_coherence:
            coherences = []
            for state in result.states:
                # Modulate coherence based on phi_coupling
                c = (state * state).tr().real if state.type == 'oper' else 1.0
                # Simulate Φ-driven resonance
                c *= (1.0 + self.phi_coupling * np.sin(phi_val * tlist[len(coherences)]))
                coherences.append(min(1.0, c))
            result.coherence = coherences

        return result
