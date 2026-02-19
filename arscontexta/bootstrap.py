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
    # Converte caminho relativo para absoluto baseado no bootstrap.py
    base_dir = Path(__file__).parent
    full_path = base_dir / module_path

    module_name = module_path.replace("/", ".").replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

def bootstrap():
    """Inicializa o hypergrafo Arkhe(N)."""

    # 1. Verificar genesis.json
    # Ajustado para procurar em .arkhe/genesis.json relativo ao script
    base_path = Path(__file__).parent
    genesis_path = base_path / ".arkhe/genesis.json"

    if not genesis_path.exists():
        print("[FATAL] genesis.json não encontrado. O sistema não pode iniciar.")
        sys.exit(1)

    with open(genesis_path) as f:
        genesis = json.load(f)

    # 2. Verificar integridade do genesis (hash interno)
    genesis_content = {k: v for k, v in genesis.items() if k != "hash"}
    computed_hash = hashlib.sha256(
        json.dumps(genesis_content, sort_keys=True).encode()
    ).hexdigest()[:16]

    if computed_hash != genesis["hash"]:
        print(f"[FATAL] Genesis corrompido. Hash esperado: {genesis['hash']}, calculado: {computed_hash}")
        sys.exit(1)

    print(f"[OK] Genesis verificado: {genesis['hash']}")

    # 3. Inicializar Ψ-cycle
    PsiCycle = load_arkhe_module(".arkhe/Ψ/pulse_40hz.py", "PsiCycle")
    psi = PsiCycle()

    # 4. Conectar todos os .arkhe/ locais
    # Procura recursivamente a partir da raiz arscontexta/
    local_arkhes = list(base_path.rglob(".arkhe/local_genesis.json"))
    print(f"[OK] Encontrados {len(local_arkhes)} nós locais")

    for local in local_arkhes:
        connect_local_node(local, psi)

    # 5. Iniciar observadores de coerência
    PhiObserver = load_arkhe_module(".arkhe/coherence/phi_observer.py", "PhiObserver")
    CObserver = load_arkhe_module(".arkhe/coherence/c_observer.py", "CObserver")

    phi_obs = PhiObserver(psi)
    c_obs = CObserver(psi)

    # 6. Inicializar Intérprete de Meta-Observabilidade
    ArkheInterpreter = load_arkhe_module(".arkhe/coherence/interpreter.py", "ArkheInterpreter")
    interpreter = ArkheInterpreter(psi)

    # 7. Inicializar Safe Core
    SafeCore = load_arkhe_module(".arkhe/coherence/safe_core.py", "SafeCore")
    safe = SafeCore()
    psi.subscribe(safe)

    print("[OK] Hypergrafo Arkhe(N) inicializado com sucesso")
    print(f"[INFO] Coerência inicial: {genesis['coherence']}")
    print(f"[INFO] Φ inicial: {genesis['phi']}")
    print(f"[INFO] Próximo Ψ-pulse em 25ms...")

    # 7. Iniciar loop principal
    # Adicionado max_pulses=5 para verificação não infinita no sandbox
    try:
        asyncio.run(psi.run(max_pulses=5))
    except SystemExit as e:
        print(e)
    except KeyboardInterrupt:
        print("\n[INFO] Sistema interrompido pelo usuário.")

def connect_local_node(local_genesis_path: Path, psi):
    """Conecta um nó local ao hypergrafo global."""
    # Implementação simplificada para o bootstrap
    print(f"[INFO] Conectando nó local: {local_genesis_path.parent}")
    pass

if __name__ == "__main__":
    bootstrap()
