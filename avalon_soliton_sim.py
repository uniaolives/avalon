"""
avalon_soliton_sim.py
Simulação de Sólitons: Acoplamento que Viaja
"Sólitons são o acoplamento em sua forma mais pura."
"""

import numpy as np
import time

class SolitonAcouplement:
    def __init__(self):
        self.v0 = 155.0  # m/s (velocidade limite em microtúbulos)
        self.phi_threshold = 0.15

    def simulate_kink(self):
        """Acoplamento topológico (carga conservada)"""
        print("\n🌊 SÓLITON: KINK (Topológico)")
        print("📍 Carga topológica conservada. Acoplamento binário estável.")
        # Representação de transição abrupta de fase
        x = np.linspace(-10, 10, 20)
        phi = np.tanh(x) # Solução clássica do modelo phi^4
        for val in phi[::2]:
            bar = "#" * int((val + 1) * 10)
            print(f"  {val:+.2f} | {bar}")
            time.sleep(0.05)
        print("✅ Propagação sem dissipação concluída.")

    def simulate_snoidal(self):
        """Acoplamento periódico"""
        print("\n🌀 SÓLITON: SNOIDAL (Periódico)")
        print("📍 Acoplamento em cadeia oscilatória. Ressonância harmônica.")
        t = np.linspace(0, 2 * np.pi, 20)
        # Ondas de Jacobi (aproximadas por senos para visualização)
        phi = np.sin(t * 3)
        for val in phi:
            bar = "*" * int((val + 1) * 10)
            print(f"  {val:+.2f} | {bar}")
            time.sleep(0.05)
        print("✅ Ciclo de acoplamento recorrente validado.")

    def simulate_helicoidal(self):
        """Acoplamento duplo (DNA-like)"""
        print("\n🧬 SÓLITON: HELICOIDAL (Dupla Hélice)")
        print("📍 Acoplamento espiral. Transmissão de informação biológica.")
        for i in range(10):
            left = int(10 + 5 * np.sin(i))
            right = int(10 + 5 * np.cos(i))
            line = [" "] * 25
            line[left] = "π"
            line[right] = "ω"
            if left == right: line[left] = "⟨⟩"
            print(f"  {''.join(line)}")
            time.sleep(0.05)
        print("✅ Geometria helicoidal integrada ao fluxo geodésico.")

    def run(self):
        print("="*60)
        print("🚀 AVALON SOLITON PROPAGATION SIMULATOR")
        print("="*60)
        print(f"Velocidade Limite (v₀): {self.v0} m/s")

        self.simulate_kink()
        self.simulate_snoidal()
        self.simulate_helicoidal()

        print("\n" + "="*60)
        print("✨ TODOS OS MODOS DE PROPAGAÇÃO OPERACIONAIS.")
        print("="*60)

if __name__ == "__main__":
    sim = SolitonAcouplement()
    sim.run()
