import numpy as np
import qutip as qt
from typing import List, Dict, Any, Union

def purity(rho: qt.Qobj) -> float:
    """Calculates the purity of a density matrix: Tr(rho^2)."""
    if rho.type == 'ket':
        return 1.0
    return (rho * rho).tr().real

def von_neumann_entropy(rho: qt.Qobj) -> float:
    """Calculates the von Neumann entropy: -Tr(rho log rho)."""
    if rho.type == 'ket':
        return 0.0
    return qt.entropy_vn(rho)

def coherence_l1(rho: qt.Qobj) -> float:
    """Calculates the l1-measure of coherence: sum_{i!=j} |rho_ij|."""
    if rho.type == 'ket':
        rho = rho * rho.dag()
    matrix = rho.full()
    return np.sum(np.abs(matrix)) - np.sum(np.abs(np.diag(matrix)))

def integrated_information(state: Union[qt.Qobj, Any]) -> float:
    """
    Simplified Integrated Information (Φ) calculation.
    Measures the interdependence between subsystems (partitioning).
    """
    # Simplified version: Φ = S(partition_A) + S(partition_B) - S(total)
    # For a single qubit, Φ is trivial. For multi-qubit, we partition.

    if not isinstance(state, qt.Qobj):
        return 0.0

    n_qubits = len(state.dims[0])
    if n_qubits < 2:
        return 0.0 # Single system has no integrated info in this simple model

    # Full entropy
    s_total = von_neumann_entropy(state)

    # 50/50 partition
    mid = n_qubits // 2
    rho_a = state.ptrace(range(mid))
    rho_b = state.ptrace(range(mid, n_qubits))

    s_a = von_neumann_entropy(rho_a)
    s_b = von_neumann_entropy(rho_b)

    phi = s_a + s_b - s_total
    return max(0.0, phi)

def coherence_trajectory_analysis(trajectory: List[float]) -> Dict[str, Any]:
    """Analyzes the statistical trends of a coherence trajectory."""
    if not trajectory:
        return {}

    arr = np.array(trajectory)
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "max": float(np.max(arr)),
        "min": float(np.min(arr)),
        "trend": float(arr[-1] - arr[0]) # Positive = gain, negative = decoherence
    }
