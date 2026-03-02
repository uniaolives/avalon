# test_swimmer.py
import numpy as np
import matplotlib.pyplot as plt
from arkhe.swimmer import FlagellarSwimmer

def test_swimmer_propulsion():
    swimmer = FlagellarSwimmer(L=10.0, A=1.0, wavelength=5.0, omega=2*np.pi,
                               C_par=0.5, C_perp=1.0, dt=0.01)

    T = 2.0
    x_hist, y_hist = swimmer.run(T)

    print(f"Final Position: ({x_hist[-1]:.4f}, {y_hist[-1]:.4f})")

    # Propulsão deve ser líquida (geralmente para trás em relação à onda)
    # Onda viaja para direita (+x), então swimmer deve ir para esquerda (-x)
    assert x_hist[-1] < 0, "Swimmer should move in negative x direction"

    plt.figure(figsize=(8,4))
    plt.plot(x_hist, y_hist, label='Body Path')
    plt.title('Microswimmer Trajectory')
    plt.savefig('swimmer_trajectory.png')
    print("✅ Swimmer Trajectory Plot saved to swimmer_trajectory.png")
    print("✅ Swimmer Test Passed")

if __name__ == "__main__":
    test_swimmer_propulsion()
