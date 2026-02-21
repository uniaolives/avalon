import numpy as np
from enum import Enum
from typing import Dict, List, Any, Callable, Optional

class Protocol(Enum):
    CONSERVATIVE = "conservative"  # Preserves mutual information
    CREATIVE = "creative"          # Increases entropy (stochastic)
    DESTRUCTIVE = "destructive"    # Decreases entropy (filtering/forgetting)
    TRANSMUTATIVE = "transmutative" # Changes category/substrate
    QUANTUM = "quantum"             # Unitary/Entanglement based

class StateSpace:
    def __init__(self, dimension: int, topology: str = "euclidean", algebra: str = "real"):
        self.dimension = dimension
        self.topology = topology
        self.algebra = algebra

    @staticmethod
    def euclidean(n: int):
        return StateSpace(dimension=n, topology="euclidean", algebra="real")

class Node:
    def __init__(self, id: str, state_space: StateSpace, initial_state: Any = None, coherence: float = 1.0, internal_dynamics: Optional[Callable] = None, attributes: Optional[Dict[str, Any]] = None, parent_id: Optional[str] = None, functions: Optional[Dict[str, str]] = None):
        self.id = id
        self.state_space = state_space
        self.current_state = np.array(initial_state) if initial_state is not None else None
        self.coherence = coherence
        self.internal_dynamics = internal_dynamics
        self.attributes = attributes or {}
        self.parent_id = parent_id
        self.functions = functions or {}
        if initial_state is not None and "state" not in self.attributes:
             self.attributes["state"] = self.current_state
        self.observables: Dict[str, Any] = {}

class Handover:
    def __init__(self, id: str, source: Node, target: Node, protocol: Protocol, map_state: Optional[Callable] = None, latency: float = 0.0, bandwidth: float = 1.0, fidelity: float = 1.0, entanglement: float = 0.0, condition: Optional[str] = None, effects: Optional[str] = None):
        self.id = id
        self.source = source
        self.target = target
        self.protocol = protocol
        self.map_state = map_state
        self.latency = latency
        self.bandwidth = bandwidth
        self.fidelity = fidelity
        self.entanglement = entanglement
        self.condition = condition
        self.effects = effects

class Constraint:
    def __init__(self, id: str, check: str, mode: str = "runtime", measurement: Optional[str] = None, on_violation: Optional[str] = None):
        self.id = id
        self.check = check
        self.mode = mode
        self.measurement = measurement
        self.on_violation = on_violation

class Hypergraph:
    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.handovers: Dict[str, Handover] = {}
        self.enums: Dict[str, Dict[str, Any]] = {}
        self.namespaces: Dict[str, List[str]] = {}
        self.dynamics: Dict[str, str] = {}
        self.constraints: Dict[str, Constraint] = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_handover(self, handover: Handover):
        self.handovers[handover.id] = handover

    def add_constraint(self, constraint: Constraint):
        self.constraints[constraint.id] = constraint
