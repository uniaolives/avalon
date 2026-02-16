# arkhenet/arkhenet_core.py
import numpy as np
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Node:
    id: int
    node_type: str
    satoshi: float = 10.0
    coherence: float = 0.9
    fluctuation: float = 0.1
    phase: float = 0.0
    position: Optional[np.ndarray] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    def update_coherence(self, delta: float):
        self.coherence += delta
        self.coherence = max(0.0, min(1.0, self.coherence))
        self.fluctuation = 1.0 - self.coherence

class DroneNode:
    def __init__(self, id: int, initial_pos: tuple):
        self.node = Node(id=id, node_type="Drone", position=np.array(initial_pos, dtype=float))
        self.mission_progress = 0.0
        self.target_position = np.array([0.0, 0.0, 0.0])

    def fly_towards_target(self, dt: float):
        if self.node.position is not None:
            direction = self.target_position - self.node.position
            dist = np.linalg.norm(direction)
            if dist > 0.1:
                speed = 1.0
                step = speed * dt
                self.node.position += (direction / dist) * min(step, dist)
                self.node.satoshi -= 0.01 * dt

    def sense(self) -> np.ndarray:
        return np.random.rand(6)

    def process(self, sensor_data: np.ndarray) -> float:
        processed = np.mean(sensor_data)
        self.node.update_coherence(0.02 * processed)
        return processed

    def act(self, processed: float):
        if processed > 0.5:
            self.mission_progress += 0.01
        self.node.satoshi += 0.001
