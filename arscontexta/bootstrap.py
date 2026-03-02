#!/usr/bin/env python3
"""
bootstrap.py — Inicialização do Hypergrafo Arkhe(N) para ARSCONTEXTA
"""

import json
import hashlib
import sys
import os
import asyncio
from pathlib import Path
import importlib.util

def load_arkhe_module(module_path, class_name):
    """Auxiliar para carregar módulos de diretórios ocultos como .arkhe."""
    base_dir = Path(__file__).parent
    full_path = base_dir / module_path
    module_name = module_path.replace("/", ".").replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

def bootstrap():
    """Inicializa o hypergrafo Arkhe(N) com fiação completa."""

    base_path = Path(__file__).parent
    genesis_path = base_path / ".arkhe/genesis.json"

    if not genesis_path.exists():
        print("[FATAL] genesis.json não encontrado.")
        sys.exit(1)

    with open(genesis_path) as f:
        genesis = json.load(f)

    # 1. Inicializar Ψ-cycle
    PsiCycle = load_arkhe_module(".arkhe/Ψ/pulse_40hz.py", "PsiCycle")
    psi = PsiCycle()

    # 2. Inicializar Safe Core
    SafeCore = load_arkhe_module(".arkhe/coherence/safe_core.py", "SafeCore")
    safe = SafeCore(node_id="GENESIS_SAFE")
    psi.subscribe(safe)

    # 3. Inicializar Rede Memética (Gossip) vinculada ao SafeCore
    MemeticNode = load_arkhe_module(".arkhe/network/memetic.py", "MemeticNode")
    genesis_memetic = MemeticNode("GENESIS_RIO", psi, safe_core=safe)

    remote_nodes = [MemeticNode(f"NODE_{i:02d}", psi, safe_core=safe) for i in range(3)]
    for node in remote_nodes:
        genesis_memetic.connect(node)
        node.connect(genesis_memetic)

    # 4. Inicializar Intérprete vinculado ao SafeCore e Rede Memética
    ArkheInterpreter = load_arkhe_module(".arkhe/coherence/interpreter.py", "ArkheInterpreter")
    interpreter = ArkheInterpreter(psi, memetic_node=genesis_memetic, safe_core=safe)

    print("[OK] Hypergrafo Arkhe(N) inicializado com fiação completa (Distributed Safe Core Enabled)")
    print(f"[INFO] Coerência inicial: {genesis['coherence']}")
    print(f"[INFO] Próximo Ψ-pulse em 25ms...")

    # 5. Iniciar loop principal
    try:
        asyncio.run(psi.run(max_pulses=10))
    except SystemExit as e:
        print(f"\n[INFO] {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Sistema interrompido pelo usuário.")

if __name__ == "__main__":
    bootstrap()
