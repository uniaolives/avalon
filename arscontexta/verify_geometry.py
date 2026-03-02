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
    print("🚀 Iniciando Verificação de Geometria Arkhe(N)...")

    base_dir = Path(__file__).parent

    # Load modules
    Manifold = load_module(base_dir / ".arkhe/geometry/manifold.py", "manifold").CharacterCountManifold
    Handover = load_module(base_dir / ".arkhe/geometry/handover.py", "handover").FeatureGeometryHandover
    SafeCore = load_module(base_dir / ".arkhe/coherence/safe_core.py", "safe_core").SafeCore
    Interpreter = load_module(base_dir / ".arkhe/coherence/interpreter.py", "interpreter").ArkheInterpreter

    # 1. Test Manifold Embedding
    print("\n--- 1. Manifold Embedding ---")
    manifold = Manifold(dimension=6)
    vec_10 = manifold.embed(10)
    print(f"Count 10 Embedding: {vec_10}")
    assert vec_10.shape == (6,), "Dimension mismatch"

    # 2. Test QK-Rotation (Simulation)
    print("\n--- 2. QK-Rotation Alignment ---")
    alignment = manifold.rotate_to_boundary(vec_10, 11)
    print(f"Alignment (10 vs 11): {alignment:.4f}")
    assert alignment > 0.9, "Alignment should be high for close values"

    # 3. Test Feature Handover
    print("\n--- 3. Geometric Handover ---")
    handover = Handover(manifold)
    features = {"count_5_15": 1.0}
    point = handover.discrete_to_continuous(features)
    print(f"Discrete -> Continuous: {point}")

    back_to_discrete = handover.continuous_to_discrete(point)
    print(f"Continuous -> Discrete: {back_to_discrete}")
    assert "count_10_15" in back_to_discrete or "count_5_10" in back_to_discrete, "Feature recovery failed"

    # 4. Test Geometric Kill Switch
    print("\n--- 4. Geometric Kill Switch ---")
    safe = SafeCore(manifold=manifold)

    # Normal state
    assert safe.check(0.05, 0.95) == True, "Should be safe"

    # Adversarial anchor
    print("Testing adversarial anchor...")
    try:
        safe.check(0.05, 0.95, anchors=['@@'])
    except SystemExit as e:
        print(f"Caught expected halt: {e}")

    # 5. Manifold Analysis
    print("\n--- 5. Manifold Analysis ---")
    interpreter = Interpreter(manifold=manifold)
    report = interpreter.analyze_manifold_state(vec_10)
    print(f"Analysis Report: {report}")
    assert report['status'] == 'NOMINAL', "Analysis failed"

    print("\n✅ Verificação de Geometria CONCLUÍDA com SUCESSO")

if __name__ == "__main__":
    try:
        verify()
    except Exception as e:
        print(f"❌ Verificação FALHOU: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
