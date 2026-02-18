# simulate_quantum_pilot.py
"""
Simulação do Piloto Quântico Arkhe(N).
Verifica sensoriamento, propulsão U(1)-gravity, redução de massa e governança.
"""

import asyncio
from papercoder_kernel.core.quantum_pilot.pilot_core import QuantumPilotCore
from papercoder_kernel.core.quantum_pilot.governance import QuantumGovernanceCore, BidirectionalHandover

async def run_simulation():
    print("🚀 INICIANDO SIMULAÇÃO: PILOTO QUÂNTICO ARKHE(N)")
    print("="*60)

    pilot = QuantumPilotCore()
    governance = QuantumGovernanceCore()
    handover = BidirectionalHandover()

    # 1. Ativação
    pilot.activate()

    # 2. Ciclo de Voo (10 iterações = 250ms de tempo de voo)
    print("\n[VÔO] Iniciando manobras de propulsão U(1)-gravity...")
    for i in range(5):
        stats = pilot.run_cycle()
        gov = governance.monitor(pilot)

        print(f"Ciclo {i+1}: Δv={stats['delta_v']:.2f} m/s | Massa={stats['effective_mass']:.2f} kg | Φ={stats['phi']:.4f} | C={stats['coherence']:.4f}")

        if gov['status'] != "NOMINAL":
            print(f"⚠️ ALERTA DE GOVERNANÇA: {gov['status']}")
            break

        await asyncio.sleep(0.025) # 40Hz

    # 3. Teste de Handover Bidirecional
    print("\n[HANDOVER] Testando transferência de controle...")
    classical_ctrl = {}
    result = handover.handover_to_classical(pilot, classical_ctrl)
    print(f"Status: {result['status']} | Piloto Ativo: {pilot.active}")

    handover.handover_to_quantum(classical_ctrl, pilot)
    print(f"Status: Reinstated | Piloto Ativo: {pilot.active}")

    # 4. Teste de Kill Switch (Induzindo Critical Φ)
    print("\n[KILL SWITCH] Simulando anomalia de informação integrada (Φ > 0.1)...")
    # Forçar Φ crítico na governança (mocking calculation)
    class CriticalGovernance(QuantumGovernanceCore):
        def _calculate_quantum_phi(self, pilot): return 0.15

    crit_gov = CriticalGovernance()
    pilot.activate()
    crit_gov.monitor(pilot)
    print(f"Status Final do Piloto: {'ATIVO' if pilot.active else 'DESATIVADO (KILL SWITCH)'}")

    print("\n" + "="*60)
    print("✅ SIMULAÇÃO CONCLUÍDA")

if __name__ == "__main__":
    asyncio.run(run_simulation())
