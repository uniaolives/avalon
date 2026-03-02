# simulate_scale_inflation.py
import numpy as np
from papercoder_kernel.core.scale_inflation import ScaleAwareInflation

def run_inflation_simulation():
    print("="*60)
    print("SIMULAÇÃO DE INFLAÇÃO SENSÍVEL À ESCALA (Fossella 2026)")
    print("="*60)

    n_scales = 10
    n_members = 20

    # Inicializa inflação
    sai = ScaleAwareInflation(n_scales=n_scales, base_inflation=1.05, sensitivity=0.8)

    # Cria um ensemble inicial com variância heterogênea entre escalas
    # Escalas baixas (0-3) têm alta variância, escalas altas (7-9) têm baixa variância
    ensemble = np.zeros((n_members, n_scales))
    for s in range(n_scales):
        scale_var = 1.0 / (s + 1)
        ensemble[:, s] = np.random.normal(loc=10.0, scale=np.sqrt(scale_var), size=n_members)

    print(f"📊 Variâncias iniciais por escala: {np.var(ensemble, axis=0, ddof=1)}")

    # Aplica inflação
    inflated = sai.apply_inflation(ensemble.copy())

    # Relatório
    report = sai.get_report()
    print(f"\n🛡️ Fatores de inflação calculados: {[round(f, 4) for f in report['scale_factors']]}")

    # Verifica se as escalas com maior variância receberam maior inflação
    factors = report['scale_factors']
    if factors[0] > factors[-1]:
        print("\n✅ Sucesso: Escalas de alta variância receberam inflação prioritária.")
    else:
        print("\n⚠️ Alerta: Distribuição de inflação inesperada.")

    print(f"\n📊 Variâncias pós-inflação: {np.var(inflated, axis=0, ddof=1)}")

    return True

if __name__ == "__main__":
    run_inflation_simulation()
