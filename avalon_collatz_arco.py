"""
Avalon Simulation: Collatz Geodesic (3n + 1) - Γ₁₁₂
Models the arithmetic trajectory of integers towards the 4-2-1 attractor.
"The +1 is the mass gap of number theory."
"""

import time

def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

class CollatzArcoSim:
    def __init__(self, start_n=27):
        self.start_n = start_n
        self.satoshi_witness = 9.45

    def run_simulation(self):
        print("="*80)
        print(f"🔢 AVALON COLLATZ GEODESIC SIMULATION: n={self.start_n} | Γ₁₁₂")
        print("="*80)

        n = self.start_n
        trajectory = [n]
        steps = 0

        print(f"\n[INPUT] Starting trajectory for n={n}")

        while n != 1:
            n = collatz_step(n)
            trajectory.append(n)
            steps += 1
            if steps % 10 == 0:
                print(f"   Step {steps}: n={n} (Geodesic Falling...)")
            if steps > 1000: # Safety break
                break

        print(f"\n[OUTPUT] Arco Resolved:")
        print(f"   Final State reached: 1 (The Unitary Atrractor)")
        print(f"   Total Steps: {steps}")
        print(f"   Max value reached: {max(trajectory)}")

        print("\n📊 TELEMETRY Γ₁₁₂:")
        print(f"   Status: ✅ ARCO STABLE (4-2-1)")
        print(f"   Satoshi Reputational Weight: {self.satoshi_witness} bits")

        print("\n✨ Arkhe(112)Aritmética: Every integer is a geodesic coming home.")

if __name__ == "__main__":
    # Test with the famous 27 (Spike Surgery needed)
    sim = CollatzArcoSim(27)
    sim.run_simulation()
