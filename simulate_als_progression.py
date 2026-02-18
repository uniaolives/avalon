# simulate_als_progression.py
import random
from papercoder_kernel.core.als_model import ALS_Hypergraph

def run_als_simulation():
    print("="*60)
    print("SIMULAÇÃO DE PROGRESSÃO ALS NO HIPERGRAFO (Γ_als)")
    print("="*60)

    # Inicializa hipergrafo com perfil de risco variado
    n_nodes = 50
    risk = 0.2
    hypergraph = ALS_Hypergraph(n_nodes=n_nodes, risk_profile=risk)

    print(f"🧬 Inicializado: {n_nodes} neurônios motores. Risco SOD1/C9orf72: {risk*100}%")

    # Simula 50 passos temporais
    for step in range(1, 51):
        hypergraph.simulate_step()
        coherence = hypergraph.get_global_coherence()
        survival = hypergraph.get_survival_rate()

        if step % 10 == 0:
            print(f"⏱️ Passo {step:02}: Coerência Global = {coherence:.4f}, Sobrevivência = {survival*100:.1f}%")

        if survival < 0.1:
            print(f"💀 Colapso Total em Passo {step}.")
            break

    print("\n🛡️ Relatório Final:")
    print(f"   Coerência Terminal: {hypergraph.get_global_coherence():.4f}")
    print(f"   Taxa de Sobrevivência: {hypergraph.get_survival_rate()*100:.1f}%")

    return hypergraph.get_survival_rate() < 1.0 # Esperamos alguma perda com risco 0.2

if __name__ == "__main__":
    run_als_simulation()
