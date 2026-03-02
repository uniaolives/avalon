# test_merkabah_cosmic.py
import asyncio
import torch
from merkabah_7 import MERKABAH7, NeutrinoEvent

async def main():
    print("🌌 Iniciando Teste de Integração Cósmica MERKABAH-7...")

    # 1. Dados do Alerta IceCube-260217A
    icecube_alert = {
        'ra': 75.89,
        'dec': 14.63,
        'energy': 100.0, # TeV
        'p_astro': 0.31,
        'far': 2.768
    }

    # 2. Setup do sistema
    corpus = [{"id": "HT 1", "lines": [[2, 5, 8, 4]]}]
    profile = {"intention": "decoding", "expertise": "high"}
    system = MERKABAH7(corpus, profile, vocab_size=11)

    # 3. Executar decifração com contexto cósmico
    print("\n🔭 Incorporando Neutrino IceCube-260217A como Modulador...")
    operator_intention = {"base_intention": "understand_linear_a"}

    result = await system.execute_with_cosmic_context(
        operator_intention=operator_intention,
        icecube_event=icecube_alert
    )

    print(f"\n🌀 Resultado da Sessão: {result['decoding']}")
    print(f"   Certeza: {result['certainty']:.4f}")

    # 4. Verificar modelagem do neutrino
    event = NeutrinoEvent(**icecube_alert)
    print(f"\n⚛️ Neutrino Wavefunction Coherence: {event.wavefunction['coherence']}")
    print(f"   Wavefunction Shape: {event.wavefunction['amplitude'].shape}")

    print("\n✅ Teste de Integração Cósmica concluído.")

if __name__ == "__main__":
    asyncio.run(main())
