import numpy as np
import qutip as qt
from arkhe_qutip import ArkheQobj, ArkheSolver, QuantumHypergraph, create_ring_hypergraph

def test_bell_state():
    print("--- Test Bell State Creation ---")
    # Create two qubits
    q0 = ArkheQobj(qt.basis(2, 0))
    q1 = ArkheQobj(qt.basis(2, 0))

    # Create hypergraph
    hg = QuantumHypergraph([q0, q1], name="Bell-state-creator")

    # Apply Hadamard to first qubit
    H_gate = (qt.sigmax() + qt.sigmaz()) / np.sqrt(2)
    q0_super = q0.handover(H_gate, {'type': 'hadamard'})
    hg.nodes[0] = q0_super

    # Apply CNOT (simulated as hyperedge)
    cnot = qt.qip.operations.cnot() if hasattr(qt, 'qip') else qt.Qobj([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dims=[[2,2],[2,2]])
    hg.add_two_qubit_gate(0, 1, cnot, weight=1.0)

    print(f"Hypergraph: {hg}")
    print(f"Node 0 coherence: {q0_super.coherence}")
    print(f"Global coherence: {hg.global_coherence:.4f}")

def test_phi_evolution():
    print("\n--- Test Φ-Driven Evolution ---")
    psi0 = ArkheQobj(qt.basis(2, 0))
    H = qt.sigmaz()
    c_ops = [0.1 * qt.sigmay()]

    # Solver with Φ coupling
    solver = ArkheSolver(H, c_ops, phi_coupling=0.05)
    tlist = np.linspace(0, 5, 50)

    result = solver.solve(psi0, tlist, track_coherence=True)

    print(f"Final coherence: {result.coherence[-1]:.4f}")
    print("Evolution complete.")

def test_ring_hypergraph():
    print("\n--- Test Ring Hypergraph ---")
    hg = create_ring_hypergraph(5)
    print(f"Ring Hypergraph: {hg}")
    stats = hg.get_topology_stats()
    print(f"Stats: {stats}")

if __name__ == "__main__":
    try:
        test_bell_state()
        test_phi_evolution()
        test_ring_hypergraph()
        print("\n✅ Verification Successful!")
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()
