import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class FlagellarSwimmer:
    """
    Simulação de um microswimmer com flagelo descrito por uma onda senoidal.
    A propulsão é estimada via Resistive Force Theory (RFT) com coeficientes
    de resistência normal (C_perp) e tangencial (C_par) (Gray & Hancock 1955).
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

        # coordenada ao longo do flagelo (0 a L)
        self.s = np.linspace(0, L, N)
        self.ds = self.s[1] - self.s[0]

        # posição inicial do flagelo (no referencial do corpo)
        # o corpo é considerado uma partícula na origem (x=0) e o flagelo
        # se estende para a direita.
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        self.t = 0.0
        self.update_shape(t=0.0)

        # posição do corpo (cabeça) no referencial inercial
        self.body_x = 0.0
        self.body_y = 0.0
        self.theta = 0.0          # orientação do corpo (não usado aqui)

        # velocidades
        self.vx = 0.0
        self.vy = 0.0

    def update_shape(self, t):
        """Atualiza a forma do flagelo no referencial do corpo."""
        # Onda viajante para a direita
        self.y = self.A * np.sin(self.k * self.s - self.omega * t)
        self.x = self.s   # aproximação inextensível (simples)

    def compute_velocity(self):
        """
        Calcula a velocidade do corpo baseado na forma e na velocidade de
        deformação do flagelo, usando RFT.
        """
        # velocidade de cada segmento no referencial do corpo
        dy_dt = -self.A * self.omega * np.cos(self.k * self.s - self.omega * self.t)
        dx_dt = np.zeros_like(dy_dt)   # o flagelo não se alonga

        # derivadas espaciais para a inclinação
        dy_ds = self.A * self.k * np.cos(self.k * self.s - self.omega * self.t)
        # a norma do vetor tangente (deve ser constante)
        norm = np.sqrt(1 + dy_ds**2)
        # cosseno e seno do ângulo local
        cos_psi = 1 / norm
        sin_psi = dy_ds / norm

        # velocidades tangencial e normal no referencial do segmento
        # (convertendo para o referencial do corpo)
        v_tang = dx_dt * cos_psi + dy_dt * sin_psi
        v_norm = -dx_dt * sin_psi + dy_dt * cos_psi

        # forças viscosas por unidade de comprimento (RFT)
        f_tang = -self.C_par * v_tang
        f_norm = -self.C_perp * v_norm

        # força total no flagelo (integrando)
        # componente x (global) = f_tang * cos_psi - f_norm * sin_psi
        # componente y (global) = f_tang * sin_psi + f_norm * cos_psi
        Fx = np.sum((f_tang * cos_psi - f_norm * sin_psi)) * self.ds
        Fy = np.sum((f_tang * sin_psi + f_norm * cos_psi)) * self.ds

        # o corpo (cabeça) sofre arrasto viscoso; assumimos uma esfera de raio R
        # com coeficiente de arrasto 6πηR, mas aqui simplificamos:
        # a força total sobre o sistema deve ser zero (corpo + flagelo)
        # então a velocidade do corpo é determinada pelo equilíbrio:
        #   -F_body = F_flagellum, com F_body = -C_body * v_body
        # Adotamos C_body = 1.0 e resolvemos v_body = F_flag / C_body
        C_body = 1.0   # ajustável
        vx_body = Fx / C_body
        vy_body = Fy / C_body

        return vx_body, vy_body

    def step(self, t):
        self.t = t
        self.update_shape(t)
        vx, vy = self.compute_velocity()
        self.body_x += vx * self.dt
        self.body_y += vy * self.dt
        # a forma do flagelo no referencial inercial é a forma no referencial do corpo
        # deslocada pela posição do corpo
        self.x_world = self.body_x + self.x
        self.y_world = self.body_y + self.y

    def run(self, T, save_animation=False):
        self.t = 0.0
        history_x = []
        history_y = []
        frames = []
        for i in range(int(T / self.dt)):
            self.step(self.t)
            history_x.append(self.body_x)
            history_y.append(self.body_y)
            if save_animation:
                frames.append((self.x_world.copy(), self.y_world.copy()))
            self.t += self.dt
        return np.array(history_x), np.array(history_y), frames

if __name__ == "__main__":
    # ========== Parâmetros da simulação ==========
    swimmer = FlagellarSwimmer(L=10.0, A=1.0, wavelength=5.0, omega=2*np.pi,
                               N=100, C_par=0.5, C_perp=1.0, dt=0.01)
    T = 10.0
    x_hist, y_hist, frames = swimmer.run(T, save_animation=True)

    # ========== Gráfico da trajetória ==========
    plt.figure(figsize=(8,4))
    plt.plot(x_hist, y_hist, 'b-', label='trajetória da cabeça')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Propulsão flagelar – trajetória')
    plt.grid(alpha=0.3)
    plt.axis('equal')
    plt.legend()
    plt.savefig('swimmer_trajectory.png', dpi=150)
    # plt.show()

    # ========== Animação ==========
    try:
        fig, ax = plt.subplots(figsize=(8,4))
        ax.set_xlim(-2, swimmer.L + 5)
        ax.set_ylim(-3, 3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(alpha=0.3)
        line, = ax.plot([], [], 'k-', lw=2)
        head, = ax.plot([], [], 'ro', markersize=8)
        tail, = ax.plot([], [], 'ko', markersize=3)

        def init():
            line.set_data([], [])
            head.set_data([], [])
            tail.set_data([], [])
            return line, head, tail

        def animate(i):
            x, y = frames[i]
            line.set_data(x, y)
            head.set_data([x[0]], [y[0]])
            tail.set_data([x[-1]], [y[-1]])
            return line, head, tail

        ani = FuncAnimation(fig, animate, frames=len(frames), init_func=init, blit=True)
        ani.save('swimmer.mp4', writer='ffmpeg', fps=50)
        plt.close()
        print("Animação salva em swimmer.mp4")
    except Exception as e:
        print(f"Não foi possível salvar a animação: {e}")
