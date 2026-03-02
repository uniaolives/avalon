import numpy as np

def sample_polynomial_roots(num_polys=100, degree=24):
    """Generate random polynomials and compute their roots (simplified)."""
    roots_list = []
    for _ in range(num_polys):
        coeffs = np.random.randn(degree+1)
        # companion matrix method
        if degree < 1:
            roots_list.append(np.array([]))
            continue

        companion = np.zeros((degree, degree))
        if degree >= 1:
            # Normalizar coeffs para evitar divisão por zero se coeffs[0] for 0
            if coeffs[0] == 0:
                coeffs[0] = 1e-10
            companion[0, :] = -coeffs[1:] / coeffs[0]
            if degree > 1:
                companion[1:, :-1] = np.eye(degree-1)
        roots = np.linalg.eigvals(companion)
        roots_list.append(roots)
    return roots_list
