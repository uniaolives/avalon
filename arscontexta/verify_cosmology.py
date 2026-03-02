import sys
from pathlib import Path
import importlib.util
import numpy as np

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def verify():
    print("🚀 Iniciando Verificação de Cosmologia Arkhe(N)...")

    base_dir = Path(__file__).parent

    # Load modules
    Maser = load_module(base_dir / ".arkhe/cosmology/maser.py", "maser").OHMaserSystem
    Lensing = load_module(base_dir / ".arkhe/cosmology/lensing.py", "lensing").GravitationalSafeCore
    Memory = load_module(base_dir / ".arkhe/cosmology/memory.py", "memory").HIMemory
    Outflow = load_module(base_dir / ".arkhe/cosmology/outflow.py", "outflow").OutflowHandover

    # 1. Test Maser System
    print("\n--- 1. OH Maser System ---")
    maser = Maser()
    seed = 1.0
    amplified = maser.mase(seed)
    print(f"Seed: {seed}, Amplified: {amplified:.4f}")
    assert amplified > seed, "Maser should amplify"

    # 2. Test Gravitational Lensing (Safe Core)
    print("\n--- 2. Gravitational Safe Core ---")
    lensing = Lensing()
    signal = 100.0
    amp_western = lensing.amplify(signal, "western_nucleus")
    print(f"Western Nucleus Amplification: {amp_western}")
    assert amp_western == 4000.0, "Western magnification should be 40x"

    # 3. Test HI Memory
    print("\n--- 3. HI Memory (Ledger) ---")
    memory = Memory()
    comparison = memory.compare_with_oh(-120)
    print(f"Comparison (OH @ -120 km/s): {comparison}")
    assert "outflow" in comparison, "Outflow detection failed"

    # 4. Test Outflow Handover
    print("\n--- 4. Outflow Handover ---")
    outflow = Outflow(oh_velocity=-120)
    h_type = outflow.handover_type()
    print(f"Handover Type: {h_type}")
    assert h_type == "NON_LOCAL_OUTFLOW", "Handover classification failed"

    print("\n✅ Verificação de Cosmologia CONCLUÍDA com SUCESSO")

if __name__ == "__main__":
    try:
        verify()
    except Exception as e:
        print(f"❌ Verificação FALHOU: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
