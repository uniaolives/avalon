# simulate_safe_core.py
"""
Simulação do Safe Core: Núcleo de Coerência Quântica.
Testa monitoramento de Φ, C, QFI e Drone Pilot.
"""

import asyncio
import numpy as np
from papercoder_kernel.core.safe_core import SafeCore
from papercoder_kernel.core.drone_pilot import DronePilot

async def run_simulation():
    print("🛡️ INICIANDO SIMULAÇÃO: SAFE CORE (ARKHE-N)")
    print("="*60)

    # 1. Teste do Safe Core Básico
    core = SafeCore(node_id="core_test_agi")
    print(f"\n[Core] Inicializado: {core.node_id}")

    # Simula evolução de estado quântico com perda de coerência
    for i in range(5):
        # Estado com ruído crescente
        q_state = np.random.randn(64) * (1.0 - 0.1 * i)
        q_state = q_state / np.linalg.norm(q_state)

        core.monitor(q_state)
        status = core.get_status()
        print(f"Passo {i+1}: Φ_q={status['phi_q']:.4f} | C={status['coherence']:.4f} | Mode={status['mode']}")

        if not status['is_active']:
            print("⚠️ Safe Core Desativado pelo Kill Switch!")
            break
        await asyncio.sleep(0.01)

    # 2. Teste do Drone Pilot com Safe Core
    print("\n[Drone] Iniciando Missão com Safe Core...")
    drone = DronePilot(drone_id="delta-01")

    for i in range(5):
        result = drone.execute_navigation_step()
        print(result)

        # Induzir falha no passo 4 (baixa coerência simulada)
        if i == 2:
            print("[Sim] Injetando ruído eletromagnético externo...")
            # Forçamos o estado para algo com baixíssima coerência média
            drone.sensors.noise_floor = 1.0

        telemetry = drone.get_telemetry()
        if not telemetry['is_active']:
            print(f"🚨 MISSÃO ABORTADA: {telemetry['node_id']} desativado.")
            break

        await asyncio.sleep(0.01)

    print("\n" + "="*60)
    print("✅ SIMULAÇÃO CONCLUÍDA")

if __name__ == "__main__":
    asyncio.run(run_simulation())
