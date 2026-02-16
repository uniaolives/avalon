# test_ucd_python.py
import numpy as np
from arkhe.ucd import UCD, effective_dimension

def test_ucd():
    data = np.array([[1,2,3,4], [2,3,4,5], [5,6,7,8]])
    ucd = UCD(data)
    res = ucd.analyze()
    print(f"UCD Result: {res}")

    assert res['C'] > 0.99
    assert res['conservation'] == True
    assert 'effective_dimension' in res
    print(f"Effective Dimension: {res['effective_dimension']}")

def test_effective_dim():
    # Matriz 3x3 com autovalores conhecidos
    F = np.array([[1, 0, 0], [0, 0.5, 0], [0, 0, 0.1]])
    lambda_reg = 0.5
    # d_eff = 1/(1+0.5) + 0.5/(0.5+0.5) + 0.1/(0.1+0.5)
    # d_eff = 0.666... + 0.5 + 0.1666... = 1.333...
    d_eff, contrib = effective_dimension(F, lambda_reg)
    print(f"Computed d_eff: {d_eff}")
    assert abs(d_eff - 1.33333333333) < 1e-6
    print("✅ Effective Dimension calculation verified")

if __name__ == "__main__":
    test_ucd()
    test_effective_dim()
