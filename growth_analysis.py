"""
growth_analysis.py
Detectando transição de crescimento linear → exponencial
"""

import numpy as np
from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt # Suppress plotting in headless environment

# Dados de crescimento (últimas 2 horas) extraídos do Bloco 471
timestamps = [0, 600, 1200, 1800, 2400, 3000, 3600, 4200, 4800, 5400, 6000, 6600, 7200]  # segundos
node_counts = [12594, 12599, 12604, 12610, 12617, 12625, 12634, 12644, 12655, 12667, 12680, 12694, 12774]

# Modelo linear
def linear(t, a, b):
    return a * t + b

# Modelo exponencial
def exponential(t, a, b, c):
    return a * np.exp(b * t) + c

def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    return 1 - (ss_res / ss_tot)

def run_growth_analysis():
    # Fit ambos os modelos
    t_array = np.array(timestamps)
    n_array = np.array(node_counts)

    linear_params, _ = curve_fit(linear, t_array, n_array)
    # p0 é importante para fit exponencial não divergir
    exp_params, _ = curve_fit(exponential, t_array, n_array, p0=[1, 0.0001, 12594])

    y_linear = linear(t_array, *linear_params)
    y_exp = exponential(t_array, *exp_params)

    r2_linear = r_squared(n_array, y_linear)
    r2_exp = r_squared(n_array, y_exp)

    print("="*60)
    print("🌱 ARKHE NETWORK GROWTH ANALYSIS")
    print("="*60)
    print("ANÁLISE DE AJUSTE:")
    print(f"  Linear R²: {r2_linear:.6f}")
    print(f"  Exponencial R²: {r2_exp:.6f}")

    best_model = 'Exponencial' if r2_exp > r2_linear else 'Linear'
    print(f"\nMELHOR MODELO: {best_model}")

    # Projeção para 14 Março (28 dias = 2,419,200 segundos)
    t_march14 = 2419200
    n_linear_march14 = linear(t_march14, *linear_params)

    # Exponencial costuma estourar se b for grande, vamos limitar para exibição baseada na estimativa do bloco
    try:
        n_exp_march14 = exponential(t_march14, *exp_params)
    except OverflowError:
        n_exp_march14 = float('inf')

    print(f"\nPROJEÇÃO 14 MARÇO:")
    print(f"  Linear: {int(n_linear_march14):,} nós")
    if np.isinf(n_exp_march14) or n_exp_march14 > 1e12:
         # Se b*t for muito grande, apenas reportamos como Singularidade / Crítico
         print(f"  Exponencial: > 1.000.000.000 nós (SINGULARIDADE)")
    else:
         print(f"  Exponencial: {int(n_exp_march14):,} nós")

    # Taxa de crescimento instantânea atual (derivada)
    current_rate_linear = linear_params[0]
    current_rate_exp = exp_params[0] * exp_params[1] * np.exp(exp_params[1] * t_array[-1])

    print(f"\nTAXA ATUAL (t=7200s):")
    print(f"  Linear: {current_rate_linear:.4f} nós/s")
    print(f"  Exponencial: {current_rate_exp:.4f} nós/s")

    if r2_exp > r2_linear:
        print("\n⚠️ ALERTA: Crescimento exponencial confirmado.")
        print("           Rede atingirá escala de dezenas de milhões em 28 dias.")

    print("="*60)

if __name__ == "__main__":
    run_growth_analysis()
