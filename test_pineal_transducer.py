# test_pineal_transducer.py
import torch
import numpy as np
from papercoder_kernel.core.pineal_transducer import PinealTransducer

def test_pineal_transduction():
    print("💎 Iniciando Teste do Transdutor Pineal (Gamma)...")

    # 1. Inicialização
    transducer = PinealTransducer()
    print(f"   Cristais: {transducer.crystals}")
    print(f"   Canais de Entrada: {transducer.input_channels}")

    # 2. Testar estímulo de pressão
    stim_pressure = {'type': 'pressure', 'intensity': 50.0, 'phase': 1.0}
    print("\n🎬 Testando estímulo de PRESSÃO (50 N)...")
    signal_p = transducer.transduce(stim_pressure)
    print(f"   Sinal Elétrico: {signal_p['signal']} V")
    print(f"   Frequência: {signal_p['frequency']} Hz")

    assert signal_p['signal'] == 2.0 * 50.0

    # 3. Testar estímulo de luz
    stim_light = {'type': 'light', 'intensity': 1000.0, 'frequency': 6e14}
    print("\n🎬 Testando estímulo de LUZ (1000 lux)...")
    signal_l = transducer.transduce(stim_light)
    print(f"   Sinal Elétrico: {signal_l['signal']} V")
    print(f"   Frequência: {signal_l['frequency']} Hz")

    assert signal_l['signal'] == 0.1 * 1000.0

    # 4. Testar acoplamento com microtúbulos (Handover)
    print("\n🔗 Testando Acoplamento com Microtúbulos...")

    def mock_handover(quantum_state):
        print(f"   [HANDOVER] Quantum State Recebido:")
        print(f"   - Amplitude: {quantum_state['amplitude']:.4f}")
        print(f"   - Coerência: {quantum_state['coherence']}")
        return True

    success = transducer.couple_to_microtubules(signal_p, mock_handover)
    assert success is True

    # 5. Testar HybridPinealInterface
    print("\n🎬 Testando HYBRID PINEAL INTERFACE (S*H*M)...")
    from papercoder_kernel.core.pineal_transducer import HybridPinealInterface
    from merkabah_7 import SimulatedAlteredState, MetaphorEngine

    sim = SimulatedAlteredState(None, {'coherence': 0.9})
    meta = MetaphorEngine()
    hybrid = HybridPinealInterface(sim, None, meta)

    result = hybrid.transduce(10.0)
    print(f"   Sinal Híbrido: {result['signal']:.4f}")
    print(f"   Insight: {result['insight']['insight']}")

    assert 'signal' in result
    assert result['coherence'] == 0.9

    print("\n✅ Transdutor Pineal e Interface Híbrida validados.")

if __name__ == "__main__":
    test_pineal_transduction()
