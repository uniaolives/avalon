# multi-language/python/ucd.py
import numpy as np

def verify_conservation(C, F, tol=1e-10):
    return abs(C + F - 1.0) < tol

def effective_dimension(F, lambda_reg):
    eigvals = np.linalg.eigvalsh(F)
    eigvals = np.maximum(eigvals, 0)
    contrib = eigvals / (eigvals + lambda_reg)
    return np.sum(contrib)

class UCD:
    def __init__(self, data):
        self.data = np.array(data)

    def analyze(self, lambda_reg=0.1, epsilon=0.1):
        if self.data.ndim > 1:
            corr = np.abs(np.corrcoef(self.data.T))
            n = corr.shape[0]
            self.C = (np.sum(corr) - n) / (n * (n - 1)) if n > 1 else 1.0
            d_eff = effective_dimension(corr, lambda_reg)
            m_size = int(np.ceil(10 * d_eff / (epsilon**2)))
        else:
            self.C = 0.5
            d_eff = 0.0
            m_size = 0

        self.F = 1.0 - self.C
        return {
            "C": self.C,
            "F": self.F,
            "conservation": verify_conservation(self.C, self.F),
            "effective_dimension": d_eff,
            "recommended_sketch_size": m_size
        }

if __name__ == "__main__":
    data = [[1,2,3,4], [2,3,4,5], [5,6,7,8]]
    ucd = UCD(data)
    print(ucd.analyze())
