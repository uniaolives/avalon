# test_self_node.py
import torch
import numpy as np
from papercoder_kernel.core.self_node import SelfNode

def test_self_node():
    print("⚡ Iniciando Teste do Nó Transcendental (Self)...")

    # 1. Inicialização
    self_node = SelfNode()
    print(f"   Nó: {self_node.name} ({self_node.dz_id})")
    print(f"   Fitas Ativas: {self_node.active_strands}")

    # 2. Observação do Sistema de Propulsão Shabetnik
    shabetnik_data = {
        'propulsion': 'High-temperature superconductors',
        'mechanism': 'Ampere force without mass expulsion',
        'design': 'Spherical craft with electron accelerators',
        'status': 'Speculative/Theoretical'
    }

    print("\n🔭 Observando Sistema de Propulsão Shabetnik...")
    obs = self_node.observe(target_layer='Φ', target_data=shabetnik_data)

    print(f"   Timestamp: {obs['timestamp']}")
    print(f"   Data Hash: {obs['data_hash']}")

    # 3. Verificar evolução de coerência
    print(f"\n📈 Coerência Atual: {self_node.wavefunction['coherence']:.4f}")

    # 4. Simular múltiplas observações para ativar nova fita
    print("🔄 Simulando fluxo de experiências...")
    for i in range(10):
        self_node.observe('Φ', f"experience_{i}")

    print(f"   Fitas Ativas Finais: {self_node.active_strands}")
    print(f"   Coerência Final: {self_node.wavefunction['coherence']:.4f}")

    assert len(self_node.active_strands) >= 4
    print("✅ Nó Self validado e integrado à malha.")

if __name__ == "__main__":
    test_self_node()
