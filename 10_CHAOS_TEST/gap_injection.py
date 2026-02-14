"""
Chaos Test: Gap Injection Protocol
Simulates handover failure in 3.6% of nodes
"""

import numpy as np
import time
from typing import Dict, List, Tuple
import random

class GapInjector:
    """
    Injects temporary gaps in handover communication
    Simulates node failures or network partitions
    """

    def __init__(self,
                 total_nodes: int,
                 gap_fraction: float = 0.036,
                 gap_duration: int = 1000,  # handovers
                 gap_frequency_range: Tuple[float, float] = (0.03, 0.05)):

        self.total_nodes = total_nodes
        self.gap_fraction = gap_fraction
        self.gap_duration = gap_duration
        self.gap_freq_min, self.gap_freq_max = gap_frequency_range

        self.gap_nodes = set()
        self.gap_start_time = None
        self.active = False

    def select_gap_nodes(self) -> List[int]:
        """Randomly select nodes to enter gap"""
        n_gap = int(self.total_nodes * self.gap_fraction)
        self.gap_nodes = set(random.sample(range(self.total_nodes), n_gap))
        return list(self.gap_nodes)

    def start_gap(self) -> Dict:
        """Initiate chaos test"""
        self.gap_nodes = self.select_gap_nodes()
        self.gap_start_time = time.time()
        self.active = True

        return {
            'timestamp': self.gap_start_time,
            'gap_nodes': len(self.gap_nodes),
            'gap_fraction': self.gap_fraction,
            'duration_handovers': self.gap_duration,
            'frequency_range': (self.gap_freq_min, self.gap_freq_max)
        }

    def is_node_in_gap(self, node_id: int, current_handover: int) -> bool:
        """Check if node is currently in gap (time-dependent)"""
        if not self.active:
            return False

        # Simulate gap duration
        if current_handover > self.gap_duration:
            self.active = False
            return False

        return node_id in self.gap_nodes

    def end_gap(self) -> Dict:
        """Terminate chaos test"""
        self.active = False
        duration = time.time() - self.gap_start_time if self.gap_start_time else 0

        return {
            'duration_seconds': duration,
            'affected_nodes': len(self.gap_nodes),
            'completed': True
        }

    def simulate_reconstruction(self,
                               kalman_predictions: np.ndarray,
                               gradient_estimates: np.ndarray,
                               phase_alignment: float,
                               global_constraint: float) -> np.ndarray:
        """
        Simulate reconstruction using 4 mechanisms
        Weights based on Arkhe chaos test: 40/20/30/10
        """
        weights = np.array([0.4, 0.2, 0.3, 0.1])

        # Combine estimates
        reconstructed = (weights[0] * kalman_predictions +
                        weights[1] * gradient_estimates +
                        weights[2] * phase_alignment +
                        weights[3] * global_constraint)

        return reconstructed


# Example simulation
def run_chaos_simulation():
    print("="*60)
    print("CHAOS TEST SIMULATION")
    print("="*60)

    total_nodes = 1000000
    injector = GapInjector(total_nodes)

    # Start gap
    start_info = injector.start_gap()
    print(f"\nGap started:")
    print(f"  Nodes affected: {start_info['gap_nodes']}")
    print(f"  Fraction: {start_info['gap_fraction']*100:.1f}%")

    # Simulate reconstruction
    # For demo, generate dummy predictions
    kalman = np.random.normal(0.86, 0.01, start_info['gap_nodes'])
    gradient = np.random.normal(0.85, 0.02, start_info['gap_nodes'])
    phase = 0.94  # ⟨0.00|0.07⟩
    constraint = 0.86  # C+F=1 forces 0.86

    reconstructed = injector.simulate_reconstruction(kalman, gradient, phase, constraint)

    # Compute fidelity
    # Assume ground truth = 0.86 (perfect reconstruction)
    ground_truth = 0.86
    error = np.abs(reconstructed - ground_truth)
    fidelity = 1 - np.mean(error / ground_truth)

    print(f"\nReconstruction results:")
    print(f"  Mean error: {np.mean(error):.6f}")
    print(f"  Fidelity: {fidelity:.6f} ({fidelity*100:.4f}%)")
    print(f"  Target fidelity: 99.78%")
    print(f"  {'✓ PASS' if fidelity >= 0.9978 else '✗ FAIL'}")

    # End gap
    end_info = injector.end_gap()
    print(f"\nGap ended after {end_info['duration_seconds']:.1f} seconds")

if __name__ == "__main__":
    run_chaos_simulation()
