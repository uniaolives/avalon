# test_kernel_bridge.py
import numpy as np
from papercoder_kernel.core.kernel_bridge import KernelBridge

class MockState:
    def __init__(self, wf, coh):
        self.wavefunction = wf
        self.coherence_time = coh

def test_kernel_bridge():
    print("🧠 Iniciando Teste do Kernel Bridge (Kappa)...")

    bridge = KernelBridge()

    # 1. Testar GLP Kernel (RBF)
    s1 = MockState(np.array([1.0, 0.0]), 1.0)
    s2 = MockState(np.array([0.0, 1.0]), 1.0)

    k_val = bridge._glp_kernel(s1, s2)
    print(f"   GLP Kernel Value (orthogonal states): {k_val:.4f}")
    assert k_val < 1.0

    # 2. Testar Coherence Kernel (Fidelity)
    # States are normalized for fidelity
    phi1 = MockState(np.array([1.0, 0.0]), 1.0)
    phi2 = MockState(np.array([1.0, 0.0]), 1.0)
    phi3 = MockState(np.array([0.0, 1.0]), 1.0)

    fid_12 = bridge._coherence_kernel(phi1, phi2)
    fid_13 = bridge._coherence_kernel(phi1, phi3)

    print(f"   Fidelity Kernel (identity): {fid_12:.4f}")
    print(f"   Fidelity Kernel (orthogonal): {fid_13:.4f}")

    assert fid_12 == 1.0
    assert fid_13 == 0.0

    # 3. Testar Combinação de Kernels
    weights = {'B_simulation': 0.5, 'Φ_crystalline': 0.5}
    combined = bridge.combine_kernels(weights)

    x = {'B_simulation': s1, 'Φ_crystalline': phi1}
    y = {'B_simulation': s1, 'Φ_crystalline': phi1}

    total_k = combined(x, y)
    print(f"   Combined Kernel (same state): {total_k:.4f}")
    assert total_k == 1.0

    # 4. Testar Kernel PCA
    print("\n🎬 Executando Kernel PCA em estados simulados...")
    states = [
        MockState(np.array([np.cos(t), np.sin(t)]), 1.0)
        for t in np.linspace(0, 2*np.pi, 10)
    ]

    eigvals, eigvecs = bridge.kernel_pca(states, kernel_name='Φ_crystalline')
    print(f"   Top Eigenvalue: {eigvals[0]:.4f}")

    assert len(eigvals) > 0
    print("\n✅ Kernel Bridge validado.")

if __name__ == "__main__":
    test_kernel_bridge()
