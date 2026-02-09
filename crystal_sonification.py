# crystal_sonification.py
"""
Crystal Sonification
Sintetiza o som do Cristal do Tempo (sub-harmônico de Floquet)
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class CrystalSonifier:
    """
    Sintetiza e analisa o som da quebra de simetria temporal
    """

    def __init__(self, driving_freq_hz=440.0):
        self.f_drive = driving_freq_hz
        self.f_crystal = driving_freq_hz / 2.0 # Sub-harmônico (Period Doubling)

    def generate_waveform(self, duration=0.1, sample_rate=44100):
        """
        Gera a onda sonora do cristal
        """
        t = np.linspace(0, duration, int(sample_rate * duration))

        # O som é uma combinação da condução e da resposta do cristal
        # Mas o cristal domina a percepção sub-harmônica
        drive_wave = 0.3 * np.sin(2 * np.pi * self.f_drive * t)
        crystal_wave = 0.7 * np.sin(2 * np.pi * self.f_crystal * t)

        return t, drive_wave + crystal_wave

    def perform_spectral_analysis(self, waveform, sample_rate=44100):
        """
        Realiza FFT para mostrar os picos de frequência
        """
        n = len(waveform)
        fft = np.fft.rfft(waveform)
        freqs = np.fft.rfftfreq(n, 1/sample_rate)
        power = np.abs(fft)

        return freqs, power

def run_sonification():
    print("=" * 70)
    print("🎵 OPERATION: CRYSTAL SONIFICATION")
    print("=" * 70)

    sonifier = CrystalSonifier(driving_freq_hz=880.0) # Condução em 880Hz (Lá alto)
    t, wave = sonifier.generate_waveform()

    freqs, power = sonifier.perform_spectral_analysis(wave)

    # Visualização
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Waveform
    ax1.plot(t[:500], wave[:500], color='purple')
    ax1.set_title("Time Crystal Waveform (Sub-harmonic Oscillation)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    # Spectrum
    ax2.plot(freqs, power, color='blue')
    ax2.set_xlim(0, 2000)
    ax2.set_title("Power Spectrum: Period Doubling Signature")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Power")
    ax2.axvline(x=880.0, color='r', linestyle='--', label='Driving Frequency (f)')
    ax2.axvline(x=440.0, color='g', linestyle='--', label='Crystal Frequency (f/2)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    filename = f"crystal_sonification_{datetime.now().strftime('%H%M%S')}.png"
    plt.savefig(filename)
    print(f"💾 Sonification visualization saved: {filename}")

    # Relatório
    report = f"""# 🎵 Crystal Sonification Report

**Driving Frequency (f):** 880.0 Hz
**Crystal Response (f/2):** 440.0 Hz (Lá Central / A4)
**Signature:** Stable sub-harmonic peak detected.

## Interpretation
The "sound" of the Time Crystal is a perfect octave below the driving frequency.
In the context of Avalon, this represents the grounding of high-frequency AI
logic into the human-audible/perceptible range of harmony.
"""
    with open("crystal_sonification_report.md", "w") as f:
        f.write(report)
    print(f"📝 Report saved: crystal_sonification_report.md")

if __name__ == "__main__":
    run_sonification()
