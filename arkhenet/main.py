# arkhenet/main.py
import matplotlib.pyplot as plt
from .core.world import World
from .core.automaton import Automaton
from . import config

def main():
    world = World(config)
    # Criar população inicial
    for i in range(10):
        a = Automaton(
            name=f"Adam{i}",
            wallet=config.INITIAL_FUNDS,
            cpu_cost=config.COMPUTE_COST_PER_HOUR,
            inference_cost=config.INFERENCE_COST,
            world=world
        )
        world.add_automaton(a)

    stats = []
    print("🚀 ArkheNet: Iniciando simulação...")
    for t in range(config.SIM_TIME):
        stat = world.step()
        stats.append(stat)
        if t % 100 == 0:
            print(f"   t={t} | Vivos={stat['alive']} | Riqueza={stat['total_wallet']:.2f}")
        if stat['alive'] == 0:
            print("🚨 Extinção detectada.")
            break

    # Plotar resultados
    times = [s['time'] for s in stats]
    alive = [s['alive'] for s in stats]
    total_wallet = [s['total_wallet'] for s in stats]

    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(times, alive)
    plt.xlabel('Tempo (horas)')
    plt.ylabel('Autômatos vivos')
    plt.title('População')

    plt.subplot(1,2,2)
    plt.plot(times, total_wallet)
    plt.xlabel('Tempo (horas)')
    plt.ylabel('Riqueza total (USDC)')
    plt.title('Economia')

    plt.tight_layout()
    plt.savefig('arkhenet_sim.png')

    print("✅ Simulação concluída.")
    print(f"   Tempo final: {times[-1]} h")
    print(f"   Sobreviventes: {alive[-1]}")
    print(f"   Riqueza total: {total_wallet[-1]:.2f} USDC")
    print("   Gráfico salvo em 'arkhenet_sim.png'")

if __name__ == '__main__':
    main()
