# test_dashavatara.py
from arkhe.dashavatara import Arkhen11

def test_dashavatara_logic():
    arkhen = Arkhen11()
    summary = arkhen.to_dict()

    print(f"Arkhen(11) Coherence: {summary['coherence']:.4f}")
    print(f"Effective Dimension: {summary['effective_dimension']:.4f}")
    print(f"Conservation (C+F=1): {summary['conservation_holds']}")

    assert summary['n_nodes'] == 11
    assert summary['conservation_holds'] == True
    assert summary['coherence'] > 0, "Coherence should be positive"
    print("✅ Dashavatara Test Passed")

if __name__ == "__main__":
    test_dashavatara_logic()
