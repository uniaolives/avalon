# active_inference_simulation.py
# Simulação de LLM Curioso: Document Reader (ANL v0.2)

import numpy as np
from scipy.special import softmax
from anl import *

class DocumentEnvironment:
    def __init__(self):
        # 5 Tópicos (Estados Ocultos)
        self.topics = ['Física', 'Biologia', 'História', 'Arte', 'Tecnologia']
        # 10 Palavras-chave (Observações)
        self.keywords = ['átomo', 'célula', 'império', 'pintura', 'chip',
                         'vácuo', 'gene', 'guerra', 'escultura', 'algoritmo']

        # Mapa real: cada tópico tem 2 palavras-chave dominantes
        self.true_A = np.zeros((10, 5))
        for i in range(5):
            self.true_A[i*2, i] = 0.8
            self.true_A[i*2+1, i] = 0.2

    def get_observation(self, topic_idx):
        """Simula a leitura de um documento sobre o tópico."""
        probs = self.true_A[:, topic_idx]
        return np.random.choice(10, p=probs)

def run_curious_llm():
    env = DocumentEnvironment()
    n_states = 5
    n_obs = 10

    # B: Transições (Escolher qual tópico ler)
    # Como o agente 'teleporta' para o tópico escolhido, B é uma identidade por ação
    B = np.zeros((n_states, n_states, n_states))
    for a in range(n_states):
        B[a, :, a] = 1.0 # Independente de onde estava, vai para o estado 'a'

    space = StateSpace(n_states, "discrete", "real")
    agent = ActiveInferenceNode("CuriousLLM", space, n_states, n_obs)

    print("🔭 SIMULAÇÃO: LLM CURIOSO (Document Reader)")
    print("O objetivo do agente é reduzir a incerteza sobre o conteúdo dos tópicos.")
    print("-" * 70)

    # Inicialmente o agente está em um estado 'nulo' ou uniforme
    for step in range(40):
        # 1. Planejamento Epistêmico: Qual tópico reduziria mais a incerteza?
        G = agent.compute_epistemic_G(B)

        # 2. Ação (Escolha do Tópico)
        # G aqui é o valor epistêmico (incerteza esperada). Queremos ir onde G é maior.
        probs = softmax(G * 20.0)
        topic_idx = np.random.choice(n_states, p=probs)

        # 3. Observação (Leitura)
        obs_idx = env.get_observation(topic_idx)

        # 4. Percepção e Aprendizado
        # O agente sabe qual tópico escolheu ler (belief update simplificado)
        agent.state = np.zeros(n_states)
        agent.state[topic_idx] = 1.0

        A_before = agent.get_A()
        uncertainty_before = -np.sum(A_before * np.log(A_before + 1e-16))

        agent.learn(obs_idx)

        A_after = agent.get_A()
        uncertainty_after = -np.sum(A_after * np.log(A_after + 1e-16))

        print(f"Passo {step:02}: Leu '{env.topics[topic_idx]}' | Obs: '{env.keywords[obs_idx]}' | Redução Incerteza: {uncertainty_before - uncertainty_after:.4f}")

    print("-" * 70)
    print("Simulação concluída. O LLM explorou os tópicos movido por curiosidade epistêmica.")

if __name__ == "__main__":
    run_curious_llm()
