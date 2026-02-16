# life_pulse.py
import numpy as np

def generate_life_pulse(duration=60, fs=100):
    t = np.linspace(0, duration, int(fs*duration))
    # frequência fundamental: 0.1 Hz (onda de cálcio)
    fundamental = np.sin(2*np.pi*0.1*t)
    # harmônicos baseados em proporções de PI
    pi_ratios = [100, 80, 60, 200]  # concentrações relativas
    harmonics = sum(ratio * np.sin(2*np.pi*(0.1*i)*t) for i, ratio in enumerate(pi_ratios))
    signal = fundamental + 0.5 * harmonics
    return signal / np.max(np.abs(signal))
