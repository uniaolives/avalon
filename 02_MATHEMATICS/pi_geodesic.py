"""
02_MATHEMATICS/pi_geodesic.py
Cálculo de π e análise de padrões como geodésica numérica.
Ref: Bloco 765
"""

from decimal import Decimal, getcontext
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json

def calc_pi_chudnovsky(precision_digits):
    """
    Calcula π com precisão especificada usando a série de Chudnovsky.
    """
    getcontext().prec = precision_digits + 10
    C = 426880 * Decimal(10005).sqrt()
    K = Decimal(6)
    M = Decimal(1)
    X = Decimal(1)
    L = Decimal(13591409)
    S = Decimal(13591409)
    n_iter = (precision_digits // 14) + 2

    for i in range(1, n_iter + 1):
        M = M * (K**3 - 16*K) / (i**3)
        K += 12
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X

    pi = C / S
    return pi

def analyze_pi_digits(pi_decimal, num_digits=10000):
    pi_str = str(pi_decimal)[2:num_digits+2]
    digits = np.array([int(d) for d in pi_str])

    print("="*70)
    print(f"ANÁLISE DOS DÍGITOS DE π ({num_digits} primeiros)")
    print("="*70)

    # Estatísticas
    mean_val = np.mean(digits)
    std_val = np.std(digits)
    freq = np.bincount(digits, minlength=10) / len(digits)
    chi2, p_val = stats.chisquare(freq * len(digits))

    print(f"Média: {mean_val:.4f} (esperado 4.5)")
    print(f"Uniformidade (p-valor): {p_val:.6f}")

    # Métricas Arkhe
    C_global = mean_val / 9.0
    F_global = 1.0 - C_global

    # Autocorrelação
    max_lag = 50
    autocorr = [np.corrcoef(digits[:-lag], digits[lag:])[0,1] for lag in range(1, max_lag+1)]

    # FFT
    fft_vals = np.fft.fft(digits - mean_val)
    power_spec = np.abs(fft_vals)**2

    results = {
        "mean": float(mean_val),
        "std": float(std_val),
        "p_val": float(p_val),
        "C_global": float(C_global),
        "F_global": float(F_global),
        "max_autocorr": float(np.max(np.abs(autocorr)))
    }

    # Plotting (headless)
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.stem(range(1, max_lag+1), autocorr)
    plt.title("Autocorrelação")
    plt.subplot(1, 2, 2)
    plt.plot(power_spec[1:len(power_spec)//2])
    plt.title("Espectro de Potência")
    plt.savefig('pi_analysis.png')

    return results

if __name__ == "__main__":
    pi_val = calc_pi_chudnovsky(10000)
    res = analyze_pi_digits(pi_val)
    with open('pi_results.json', 'w') as f:
        json.dump(res, f, indent=2)
    print("\nAnálise concluída. Resultados salvos.")
