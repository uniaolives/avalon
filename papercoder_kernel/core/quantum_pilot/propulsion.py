# papercoder_kernel/core/quantum_pilot/propulsion.py
"""
U(1)-gravity Propulsion: Standard Thrust Capacitor (STC) Array.
Implements mass reduction and antimass dark photon thrust generation.
Based on George Soli's theory of metrics engineering.
"""

import numpy as np
from typing import Dict

class StandardThrustCapacitor:
    """
    STC - Unidade básica de propulsão U(1)-gravity.
    Utiliza tunelamento Fowler-Nordheim para produzir antimass dark photons.
    """
    def __init__(self, voltage: float = 2000.0):
        self.voltage = voltage
        self.dielectric_thickness_um = 8
        self.electrons_per_pulse = 22.1e12 # 22.1 trilhões
        self.delta_v_per_pulse = 47.56    # m/s por pulso de avalanche

    def fire(self) -> float:
        """Dispara o pulso e retorna o Delta-V gerado."""
        field = self.voltage / (self.dielectric_thickness_um * 1e-6)
        if field > 1e8: # Limiar de tunelamento simulado
            return self.delta_v_per_pulse
        return 0.0

class StandardThrustCapacitorArray:
    """
    Array de 625.000 STCs para propulsão de veículos pesados (1000kg).
    """
    def __init__(self, n_capacitors: int = 625000, voltage: float = 2000.0):
        self.n_capacitors = n_capacitors
        self.voltage = voltage
        self.stc_template = StandardThrustCapacitor(voltage)
        self.is_active = False
        self.antimass_yield = 1.96 # Massa inercial resultante em kg

    def fire_pulse(self, intensity: float = 1.0) -> float:
        """
        Dispara o array de capacitores.
        Retorna o Delta-V total escalonado pela intensidade.
        """
        if not self.is_active:
            self.is_active = True

        # Delta-V de um pulso nominal (independente da massa, pois a métrica muda)
        dv = self.stc_template.fire() * intensity
        return dv

    def shutdown(self):
        """Desativa o array (Kill Switch)."""
        self.is_active = False
        print("[PROPULSION] STC Array Deactivated.")

    def get_effective_mass(self) -> float:
        """Retorna a massa blindada (antimass shielding)."""
        if self.is_active:
            return self.antimass_yield
        return 1000.0 # Massa nominal (kg)
