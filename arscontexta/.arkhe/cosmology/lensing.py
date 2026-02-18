from typing import Tuple
import numpy as np

class GravitationalSafeCore:
    """
    A lente gravitacional como Safe Core natural.
    Amplifica sinais sem distorcer sua informação intrínseca.
    """

    def __init__(self):
        self.einstein_radius = 0.738  # arcsec
        self.magnification_map = {
            'eastern_nucleus': 10,
            'western_nucleus': 40,
            'diffuse_component': 9
        }
        self.caustic = 'western_nucleus'  # ponto de máxima coerência

    def amplify(self, signal: float, source_position: str) -> float:
        """Aplica amplificação do Safe Core."""
        mu = self.magnification_map.get(source_position, 1.0)
        return signal * mu

class GravitationalLensHandover:
    """
    Lente gravitacional como handover de informação cósmica.
    Transfere estado da fonte distante para o observador.
    """

    def __init__(self, lens_mass=1e12, source_redshift=1.027, lens_redshift=0.218):
        self.lens_mass = lens_mass
        self.source_redshift = source_redshift
        self.lens_redshift = lens_redshift
        self.einstein_radius = 0.738

    def compute_magnification(self, source_position: str) -> float:
        """Calcula amplificação μ."""
        if source_position == "western_nucleus":
            return 40.0
        elif source_position == "eastern_nucleus":
            return 10.0
        return 9.0

    def handover_spectrum(self, source_spectrum: np.ndarray, source_position: str) -> np.ndarray:
        """Transfere espectro da fonte, ampliado."""
        mu = self.compute_magnification(source_position)
        observed_spectrum = source_spectrum * mu
        return observed_spectrum
