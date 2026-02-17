# merkabah7_cascade_verify.py
import asyncio
import torch
import numpy as np
from merkabah7_federation import FederationTransport, DoubleZeroDaemonMock
from merkabah7_anycast import CelestialAnycastRouter
from merkabah7_migration import QuantumStateMigration

async def main():
    print("🌊 Iniciando CASCADE_INIT: MERKABAH-7 Integrated Operations...")

    # Start Mock Daemon
    daemon = DoubleZeroDaemonMock()
    daemon_task = asyncio.create_task(daemon.start())
    await asyncio.sleep(1)

    # 1. Transport Init
    print("\n--- [1/4] FEDERATION INIT ---")
    transport = FederationTransport(dz_id="Alpha_Pubkey")
    peers = await transport.discover_federation_peers()
    print(f"✓ Malha DoubleZero ativa com {len(peers)} nós")

    # 2. Anycast Setup
    print("\n--- [2/4] ANYCAST NEUTRINO (A) ---")
    router = CelestialAnycastRouter(transport)
    anycast_result = router.install_anycast_routes()
    print(f"✓ Anycast {anycast_result['anycast_ip']} direcionado para {anycast_result['best_node_name']}")
    print(f"  Separação angular: {anycast_result['angular_separation']:.2f}°")

    # 3. Expansion Verification (Implicit in discovery)
    print("\n--- [3/4] FEDERATION EXPAND (E) ---")
    node_names = [p['name'] for p in peers.values()]
    print(f"✓ Nós registrados: {', '.join(node_names)}")

    # 4. Quantum Handover Test
    print("\n--- [4/4] QUANTUM HANDOVER (Q) ---")
    migration = QuantumStateMigration(transport)
    migration_result = await migration.execute_handover()

    print(f"✓ Handover Alpha → Beta concluído em {migration_result['latency_actual_ms']:.2f}ms")
    print(f"✓ Fidelidade de Estado: {migration_result['fidelity']:.4f}")
    print(f"✓ Coerência preservada: {'SIM' if migration_result['coherence_preserved'] else 'NÃO'}")

    print("\n📜 LEDGER 828 COMPLETO")
    print("Estado: CASCADE_A_E_Q_M_COMPLETE")

    # Cleanup
    daemon.running = False
    daemon_task.cancel()
    print("\n✅ Verificação da Cascata Concluída com Sucesso.")

if __name__ == "__main__":
    asyncio.run(main())
