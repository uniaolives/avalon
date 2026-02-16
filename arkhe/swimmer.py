# arkhe/swimmer.py
"""
Parametric Flagellar Propulsion: Trigonometric Simulation of Synthetic Microswimmers.
(Γ_swimmer)
"""

import numpy as np
from typing import List, Tuple, Optional

class FlagellarSwimmer:
    """
    Simulação de um microswimmer com flagelo descrito por uma onda senoidal.
    A propulsão é estimada via Resistive Force Theory (RFT).
    """
    def __init__(self, L=10.0, A=1.0, wavelength=5.0, omega=2*np.pi, N=100,
                 C_par=1.0, C_perp=2.0, dt=0.01):
        self.L = L
        self.A = A
        self.k = 2*np.pi / wavelength
        self.omega = omega
        self.N = N                      # número de segmentos
        self.C_par = C_par
        self.C_perp = C_perp
        self.dt = dt
        self.t = 0.0

        # coordenada ao longo do flagelo (0 a L)
        self.s = np.linspace(0, L, N)
        self.ds = self.s[1] - self.s[0]

        # posição inicial do flagelo (no referencial do corpo)
        self.x = self.s   # aproximação inextensível (simples)
        self.y = np.zeros(N)

        # posição do corpo (cabeça) no referencial inercial
        self.body_x = 0.0
        self.body_y = 0.0

    def update_shape(self, t: float):
        """Atualiza a forma do flagelo no referencial do corpo."""
        self.y = self.A * np.sin(self.k * self.s - self.omega * t)

    def compute_velocity(self) -> Tuple[float, float]:
        """
        Calcula a velocidade do corpo baseado na RFT.
        """
        # velocidade de cada segmento no referencial do corpo
        dy_dt = -self.A * self.omega * np.cos(self.k * self.s - self.omega * self.t)
        dx_dt = np.zeros_like(dy_dt)

        # derivadas espaciais para a inclinação
        dy_ds = self.A * self.k * np.cos(self.k * self.s - self.omega * self.t)
        norm = np.sqrt(1 + dy_ds**2)

        cos_psi = 1 / norm
        sin_psi = dy_ds / norm

        v_tang = dx_dt * cos_psi + dy_dt * sin_psi
        v_norm = -dx_dt * sin_psi + dy_dt * cos_psi

        # forças viscosas por unidade de comprimento
        f_tang = -self.C_par * v_tang
        f_norm = -self.C_perp * v_norm

        # força total no flagelo
        Fx = np.sum((f_tang * cos_psi - f_norm * sin_psi)) * self.ds
        Fy = np.sum((f_tang * sin_psi + f_norm * cos_psi)) * self.ds

        # Equilíbrio de força com o corpo (C_body = 1.0)
        C_body = 1.0
        vx_body = Fx / C_body
        vy_body = Fy / C_body

        return float(vx_body), float(vy_body)

    def step(self):
        self.update_shape(self.t)
        vx, vy = self.compute_velocity()
        self.body_x += vx * self.dt
        self.body_y += vy * self.dt
        self.t += self.dt

    def run(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        steps = int(duration / self.dt)
        x_hist = np.zeros(steps)
        y_hist = np.zeros(steps)

        for i in range(steps):
            x_hist[i] = self.body_x
            y_hist[i] = self.body_y
            self.step()

        return x_hist, y_hist
