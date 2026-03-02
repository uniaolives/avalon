# simulate_deep_braid.py
import numpy as np
from papercoder_kernel.core.deep_braid import DeepBraidArchitecture

def run_p61_simulation():
    print("="*60)
    print("SIMULAÇÃO DE TRANÇA PROFUNDA (p=61) - ARQUITETURA MERSENNE")
    print("="*60)

    # Instanciar para p=61 (Primo de Mersenne)
    try:
        braid = DeepBraidArchitecture(p=61)
        print(f"✅ Arquitetura inicializada para p={braid.p}")

        # Gerar palavra da trança
        word = braid.generate_braid_word()
        print(f"📦 Palavra da trança gerada. Comprimento: {len(word)}")
        print(f"   Primeiros 20 geradores: {word[:20]}...")

        # Calcular invariantes
        invariants = braid.compute_invariants()
        print(f"💎 Invariante de Jones: {invariants['jones']}")
        print(f"🧬 Invariante HOMFLY-PT: {invariants['homfly']}")
        print(f"📊 Razão de Estabilidade: {invariants['stability']:.6f}")

        # Verificar estabilidade
        stable = braid.stability_check()
        print(f"🛡️ Status de Proteção: {'PROTEGIDO (Mersenne OK)' if stable else 'FALHA DE COERÊNCIA'}")

        # Executar ciclo completo
        report = braid.execute_braid()
        print(f"\n📜 Relatório Final: {report}")

        return stable
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")
        return False

if __name__ == "__main__":
    success = run_p61_simulation()
    if success:
        print("\n✅ Simulação concluída com sucesso. Densidade sustentada.")
    else:
        print("\n❌ Simulação falhou.")
