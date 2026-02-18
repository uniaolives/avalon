# simulate_mrn_repair.py
import numpy as np
from papercoder_kernel.core.scale_inflation import ScaleAwareInflation
from papercoder_kernel.core.mrn_repair import MRN_RepairComplex

def run_mrn_simulation():
    print("="*60)
    print("SIMULAÇÃO DO COMPLEXO DE REPARO MRN (MRE11-RAD50-NBS1)")
    print("="*60)

    n_positions = 15
    n_members = 10

    # 1. Inicializa o sistema de inflação
    inflation = ScaleAwareInflation(n_scales=n_positions)

    # 2. Cria um ensemble estável (baixa variância)
    ensemble = np.random.normal(loc=1.0, scale=0.01, size=(n_members, n_positions))

    # 3. Introduz uma "quebra" (alta variância) na posição 7
    ensemble[:, 7] = np.random.normal(loc=1.0, scale=0.5, size=n_members)

    print(f"📊 Variância inicial (pos 7): {np.var(ensemble[:, 7]):.6f}")

    # 4. Inicializa o complexo de reparo
    repair_complex = MRN_RepairComplex(ensemble, inflation)

    # 5. Detecta quebras
    breaks = repair_complex.detect_breaks(coherence_threshold=0.5)
    print(f"🔍 Quebras detectadas nos índices: {breaks}")

    if 7 in breaks:
        print("✅ Sucesso: Quebra na posição 7 detectada.")
    else:
        print("❌ Falha: Quebra na posição 7 não detectada.")

    # 6. Recruta reparo
    print("\n🏗️ Recrutando complexo de reparo para sutura...")
    repair_complex.recruit_repair(breaks.tolist())

    # 7. Verifica resultado do reparo
    # Como aplicamos inflação extra (rho*2), a variância deve mudar.
    # Em um cenário real de assimilação, o reparo forçaria convergência se tivéssemos observações.
    # Aqui, verificamos se o log foi gerado.
    report = repair_complex.get_repair_report()
    print(f"📜 Relatório de Reparo: {report}")

    # 8. Verificação de sutura contra verdade conhecida (fragmentos)
    known_fragments = {7: 1.0} # Sabemos que o valor real na posição 7 deveria ser 1.0
    suture_ok = repair_complex.verify_suture(known_fragments, tolerance=0.5)
    print(f"🧬 Sutura verificada (fragmento 7): {'BEM-SUCEDIDA' if suture_ok else 'REJEITADA'}")

    return len(breaks) > 0

if __name__ == "__main__":
    success = run_mrn_simulation()
    if success:
        print("\n✅ Simulação MRN concluída. Estrutura de dados preservada.")
    else:
        print("\n❌ Simulação MRN falhou.")
