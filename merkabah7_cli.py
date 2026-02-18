# merkabah7_cli.py
import asyncio
import sys
import argparse
from merkabah7_federation import FederationTransport, DoubleZeroDaemonMock
import torch

async def broadcast(blocks, peers, urgency):
    print(f"📡 Iniciando BROADCAST CRÍTICO para blocos {blocks}...")

    # Start mock daemon in background
    daemon = DoubleZeroDaemonMock()
    daemon_task = asyncio.create_task(daemon.start())
    await asyncio.sleep(0.5)

    transport = FederationTransport(dz_id="Rafael_Node_Alpha_NY5")
    await transport.discover_federation_peers()

    for block_id in blocks.split(','):
        proposal = {
            'block': block_id,
            'state': {'wavefunction': torch.randn(128), 'layer': 'HYPOTHESIS'},
            'parents': [str(int(block_id)-1)]
        }
        print(f"\n--- Transmitindo Bloco {block_id} ---")
        success = await transport.run_consensus_round(proposal)
        if success:
            print(f"✅ Bloco {block_id} sincronizado com a federação.")
        else:
            print(f"❌ Falha no consenso do bloco {block_id}.")

    daemon.running = False
    daemon_task.cancel()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--blocks")
    parser.add_argument("--peers")
    parser.add_argument("--urgency")

    args = parser.parse_args()

    if args.command == "broadcast":
        await broadcast(args.blocks, args.peers, args.urgency)

if __name__ == "__main__":
    asyncio.run(main())
