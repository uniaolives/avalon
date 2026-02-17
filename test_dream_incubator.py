# test_dream_incubator.py
import torch
import asyncio
import numpy as np
from glp_second_quantization import BCD_GLPLinearA
from dream_linear_a import DreamIncubatorGLP, LucidInterface

async def main():
    print("🚀 Iniciando Teste de Incubação Onírica...")

    # 1. Setup do modelo
    vocab_size = 11
    model = BCD_GLPLinearA(vocab_size=vocab_size)

    # 2. Inicialização do Incubador
    incubator = DreamIncubatorGLP(model)
    lucid = LucidInterface(incubator)

    # 3. Sequência de teste (Linear A)
    # [a, ka, ru, ja] -> [2, 5, 8, 4]
    sequence = torch.tensor([[2, 5, 8, 4]])

    # 4. Incubação em estado REM
    print("\n💤 Incubando em estado REM...")
    result_rem = await incubator.incubate_sequence(sequence, target_state='REM')

    print(f"   Visibilidade Quântica: {result_rem['quantum_contribution']:.4f}")
    print(f"   Confiança do Insight: {result_rem['confidence']:.4f}")

    # 5. Interface Lúcida
    print("\n✨ Entrando em Sonho Lúcido...")
    result_lucid = await lucid.enter_lucid_state(sequence)

    print(f"   Visibilidade Quântica (Lúcido): {result_lucid['quantum_contribution']:.4f}")
    print(f"   Regiões de Insight: {result_lucid['representation'].shape}")

    # 6. Injeção de Intenção
    print("\n🎯 Injetando Intenção Semântica...")
    # Intenção de focar em uma escala específica (ex: escala 3)
    intention = torch.zeros_like(model.tunneling.resonance_energy)
    intention[1, :] = 1.0
    lucid.inject_intention(intention)

    print("✅ Teste concluído com sucesso.")

if __name__ == "__main__":
    asyncio.run(main())
