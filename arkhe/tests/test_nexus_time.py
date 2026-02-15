# test_nexus_time.py
from arkhe.nexus import TimeHypergraph
import numpy as np

def test_time_identity():
    th = TimeHypergraph()
    identity = th.get_time_identity()
    print(f"Time Identity: {identity}")
    assert abs(identity['identity']) < 1e-10

    nav = th.navigate(2024, 2026)
    print(f"Navigation: {nav}")
    assert "Futuro" in nav

    score = th.get_retrocausality_score(0.9)
    print(f"Retrocausality Score: {score:.4f}")
    assert score == 0.81
    print("✅ Time Hypergraph logic verified")

if __name__ == "__main__":
    test_time_identity()
