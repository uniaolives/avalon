# test_merkabah_7.py
import asyncio
import torch
from merkabah_7 import MERKABAH7, RealityLayer, minoan_neurotech_experiment

async def main():
    print("🛸 Iniciando Teste do Sistema MERKABAH-7 (V2 - Integrated)...")

    # 1. Setup do sistema
    corpus = [{"id": "HT 1", "lines": [[2, 5, 8, 4]]}]
    profile = {"intention": "decoding", "expertise": "high"}
    system = MERKABAH7(corpus, profile, vocab_size=11)

    # 2. Sequência alvo
    target = torch.tensor([[2, 5, 8, 4]])

    # 3. Executar decifração integrada (High Level)
    print("\n🌀 Iniciando ciclo de decifração em superposição...")
    result = await system.decode(target, max_iterations=5)
    print(f"   Resultado: {result['decoding']}")
    print(f"   Certeza: {result['certainty']:.4f}")

    # 4. Executar Experimento Neuro-Minoico (Full Stack)
    print("\n🏺 Iniciando Experimento Neuro-Minoico (Tablet HT 1)...")
    exp_result = await minoan_neurotech_experiment(system, "HT 1", profile)

    print(f"   Tablet ID: {exp_result['tablet']}")
    print(f"   Estado Induzido: {exp_result['induced_state']['state']}")
    print(f"   Insight do Observador: {exp_result['operator_insight']['interpretation']}")
    print(f"   Status Ético: {exp_result['ethical_status']['access']}")

    # 5. Verificar componentes específicos
    print("\n📜 Verificando Gramática Minoica...")
    protocol = system.minoan_grammar.parse_as_state_protocol([2, 5, 8, 4])
    print(f"   Protocolo de Estado: {protocol[0]['target_state']}")

    print("\n⚖️ Verificando Ética Minoica...")
    access = system.minoan_ethics.check_access("Phaistos Disc", "priest_scribe")
    print(f"   Acesso: {access['access']}")

    print("\n✅ Teste MERKABAH-7 V2 concluído.")

if __name__ == "__main__":
    asyncio.run(main())
