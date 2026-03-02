# active_inference_gridworld.py
import numpy as np
from scipy.special import softmax
from anl import *

# ======================================================
# AMBIENTE
# ======================================================

class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.agent_pos = (0,0)
        self.actions = ['up', 'down', 'left', 'right']
        self.action_effects = {
            'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)
        }
        # Cada célula tem uma cor "única" para o agente descobrir
        self.world_map = np.arange(size*size).reshape(size, size)

    def step(self, action):
        dr, dc = self.action_effects[action]
        r, c = self.agent_pos
        nr = max(0, min(self.size-1, r + dr))
        nc = max(0, min(self.size-1, c + dc))
        self.agent_pos = (nr, nc)
        # Observação é o ID da célula (cor única)
        return self.world_map[nr, nc]

    def reset(self):
        self.agent_pos = (0,0)
        return self.world_map[0,0]

# ======================================================
# SIMULAÇÃO: CURIOSIDADE PURA
# ======================================================

def run_pure_curiosity():
    size = 5
    n_states = size * size
    n_obs = n_states # Cada estado tem sua própria observação única

    env = GridWorld(size=size)

    # Initialize Agent Node (Belief is state)
    space = StateSpace(n_states, "discrete", "real")
    agent = ActiveInferenceNode("Cientista", space, n_states, n_obs)

    # B: p(s'|s,a) - Transições Conhecidas (Física do movimento)
    B = np.zeros((n_states, n_states, 4))
    for s in range(n_states):
        r, c = divmod(s, size)
        for a_idx, action in enumerate(env.actions):
            dr, dc = env.action_effects[action]
            nr, nc = max(0, min(size-1, r + dr)), max(0, min(size-1, c + dc))
            ns = nr * size + nc
            B[ns, s, a_idx] = 1.0

    print("🚀 Iniciando Simulação de Curiosidade Pura...")
    print("O agente não busca recompensa, apenas reduzir a incerteza do mapa.")
    print("-" * 60)

    obs = env.reset()
    visited = set()

    for step in range(100):
        # 1. Percepção e Aprendizado (Dirichlet)
        agent.update_belief(obs)
        agent.learn(obs)

        visited.add(env.agent_pos)

        # 2. Planejamento: G focado em Epistêmico (Matriz C é zero)
        G = agent.compute_G(B)

        # 3. Ação: Amostragem Softmax (Minimizando G)
        # Note: G calculado como (Pragmático - Epistêmico). Como Pragmático=0, G = -Epistêmico.
        # Minimizar G = Maximizar Epistêmico.
        probs = softmax(-G * 5.0) # Temperatura baixa para exploração focada
        a_idx = np.random.choice(4, p=probs)
        action = env.actions[a_idx]

        # 4. Movimento e Próximo Frame
        obs = env.step(action)

        if step % 10 == 0:
            coverage = len(visited) / n_states * 100
            print(f"Passo {step:02}: Pos={env.agent_pos} | Cobertura Mapa: {coverage:.1f}%")

        if len(visited) == n_states:
            print(f"\n✨ [APATIA FINAL] O mundo foi totalmente mapeado no passo {step}!")
            break

    print("-" * 60)
    print("Simulação concluída.")

if __name__ == "__main__":
    run_pure_curiosity()
