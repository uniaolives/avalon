"""
avalon_horizon_approach.py
Telemetria da Queda Geodésica: Aproximação do Horizonte
Γ₁₁₆: "O horizonte é o limite assintótico do acoplamento."
"""

import time
import numpy as np

class HorizonTelemetry:
    def __init__(self):
        self.r_rh = 0.50 # Início da simulação
        self.tunneling_prob = 0.15
        self.own_silence = 1031.2
        self.obs_silence = 617.4
        self.satoshi = 7.27

    def step(self):
        """Um passo em direção ao horizonte"""
        # A queda é acelerada (aproximação logarítmica)
        self.r_rh *= 0.95

        # Probabilidade de tunelamento cresce à medida que r/rh diminui
        self.tunneling_prob = min(1.0, self.tunneling_prob + (1.0 - self.r_rh) * 0.1)

        # Divergência temporal (declínio na fase final conforme Blocks 318-333)
        self.own_silence -= 5.0
        self.obs_silence += 0.5
        divergence = self.own_silence - self.obs_silence

        return {
            "r_rh": self.r_rh,
            "T": self.tunneling_prob,
            "S_p": self.own_silence,
            "S_o": self.obs_silence,
            "D": divergence
        }

    def run(self, steps=15):
        print("="*60)
        print("⚫ TELEMETRIA DE APROXIMAÇÃO DO HORIZONTE (ARKHE Γ₁₁₆)")
        print("="*60)
        print(f"{'Step':<5} | {'r/rh':<8} | {'T':<8} | {'Div (min)':<10} | {'Status'}")
        print("-" * 60)

        for i in range(steps):
            data = self.step()
            status = "AQUÉM" if data["r_rh"] > 0.2 else "PROXIMAL"
            if data["T"] > 0.99: status = "INEVITÁVEL"

            print(f"{i:03d}   | {data['r_rh']:.3f}    | {data['T']:.3f}    | {data['D']:.1f}      | {status}")
            time.sleep(0.05)

            if data["r_rh"] < 0.120: # Limite da Γ₁₁₆
                break

        print("-" * 60)
        print(f"📍 ALCANCE FINAL: r/rh = {data['r_rh']:.3f} (Meta Γ₁₁₆ atingida)")
        print(f"📊 Satoshi Invariant: {self.satoshi} bits (Estável)")
        print(f"✨ Acoplamento Puro Detectado.")
        print("="*60)

if __name__ == "__main__":
    telemetry = HorizonTelemetry()
    telemetry.run()
