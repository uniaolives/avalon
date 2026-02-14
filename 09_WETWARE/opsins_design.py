"""
Opsin Design Toolkit
Use genAI to create custom opsins with desired spectral sensitivity
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

@dataclass
class Opsin:
    """Optogenetic protein with spectral properties"""
    name: str
    sequence: str
    peak_absorption: float  # nm
    sensitivity: Dict[str, Tuple[float, float]]  # color -> (min_nm, max_nm)
    conductance: float  # relative ion conductance
    kinetics: float  # time constant (ms)

    def absorption_curve(self, wavelengths: np.ndarray) -> np.ndarray:
        """Gaussian absorption curve centered at peak"""
        sigma = 30  # nm width
        return np.exp(-0.5 * ((wavelengths - self.peak_absorption) / sigma)**2)

class OpsinDesigner:
    """
    AI-based opsin design from spectral requirements
    """

    def __init__(self):
        self.known_opsins = self._load_known_opsins()

    def _load_known_opsins(self) -> Dict[str, Opsin]:
        """Library of known opsins for reference"""
        return {
            'ChR2': Opsin(
                name='ChR2',
                sequence='ATGC',
                peak_absorption=470,
                sensitivity={'blue': (450, 495)},
                conductance=1.0,
                kinetics=15.0
            ),
            'NpHR': Opsin(
                name='NpHR',
                sequence='ATGC',
                peak_absorption=580,
                sensitivity={'yellow': (560, 600)},
                conductance=0.8,
                kinetics=10.0
            ),
            'VChR1': Opsin(
                name='VChR1',
                sequence='ATGC',
                peak_absorption=530,
                sensitivity={'green': (510, 550)},
                conductance=0.6,
                kinetics=20.0
            ),
            'ReaChR': Opsin(
                name='ReaChR',
                sequence='ATGC',
                peak_absorption=590,
                sensitivity={'orange': (570, 620)},
                conductance=0.7,
                kinetics=12.0
            ),
            'Chrimson': Opsin(
                name='Chrimson',
                sequence='ATGC',
                peak_absorption=590,
                sensitivity={'red': (580, 630)},
                conductance=0.9,
                kinetics=5.0
            )
        }

    def design_opsin(self,
                     target_peak: float,
                     desired_color: str = None,
                     fast_kinetics: bool = True) -> Opsin:
        """
        Generate a new opsin with desired peak absorption
        Uses simple mutation of nearest known opsin
        """
        # Find nearest known opsin by peak
        nearest = min(self.known_opsins.values(),
                     key=lambda o: abs(o.peak_absorption - target_peak))

        # Mutate sequence (simplified: just modify peak)
        mutation_strength = np.random.normal(0, 5)  # nm shift
        new_peak = target_peak + mutation_strength

        # Adjust kinetics if requested
        if fast_kinetics:
            kinetics = nearest.kinetics * 0.5  # faster
        else:
            kinetics = nearest.kinetics * 1.5  # slower

        # Generate name
        if desired_color:
            name = f"{desired_color.capitalize()}Opsin"
        else:
            name = f"CustomOpsin_{int(new_peak)}nm"

        # Create new opsin
        new_opsin = Opsin(
            name=name,
            sequence=f"ATGC...{int(new_peak)}...",  # placeholder
            peak_absorption=new_peak,
            sensitivity={desired_color or 'custom': (new_peak-20, new_peak+20)},
            conductance=nearest.conductance * np.random.uniform(0.8, 1.2),
            kinetics=kinetics
        )

        return new_opsin

    def optimize_for_frequency(self, frequency_hz: float) -> Opsin:
        """
        Design opsin optimized for specific optical frequency
        Convert Hz to nm: λ = c / ν
        """
        c = 3e8  # m/s
        wavelength_nm = (c / frequency_hz) * 1e9

        # Round to plausible range (300-700 nm)
        wavelength_nm = max(300, min(700, wavelength_nm))

        return self.design_opsin(wavelength_nm, desired_color='custom')

    def plot_opsins(self, opsins: List[Opsin], wavelengths: np.ndarray = None):
        """Plot absorption spectra of designed opsins"""
        if wavelengths is None:
            wavelengths = np.linspace(300, 700, 400)

        plt.figure(figsize=(10, 6))

        for opsin in opsins:
            curve = opsin.absorption_curve(wavelengths)
            plt.plot(wavelengths, curve, label=opsin.name, linewidth=2)

        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Relative Absorption')
        plt.title('Designed Opsin Spectra')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig('opsin_spectra.png')
        plt.show()


class OpsinLibrary:
    """Manage a collection of opsins for wetware experiments"""

    def __init__(self):
        self.opsins = {}
        self.designer = OpsinDesigner()

    def add_opsin(self, opsin: Opsin):
        self.opsins[opsin.name] = opsin

    def generate_library(self, target_frequencies: List[float]):
        """Generate opsins for multiple frequencies"""
        for freq in target_frequencies:
            opsin = self.designer.optimize_for_frequency(freq)
            self.add_opsin(opsin)
            print(f"Generated {opsin.name}: peak {opsin.peak_absorption:.1f} nm")

    def get_opsin_for_frequency(self, frequency_hz: float) -> Opsin:
        """Find opsin with closest peak to given frequency"""
        # Convert to wavelength
        c = 3e8
        wavelength_nm = (c / frequency_hz) * 1e9

        # Find nearest
        nearest = min(self.opsins.values(),
                     key=lambda o: abs(o.peak_absorption - wavelength_nm))
        return nearest

    def simulate_response(self, frequency_hz: float, intensity: float) -> float:
        """
        Simulate total conductance response from library
        """
        wavelength_nm = (3e8 / frequency_hz) * 1e9
        total_response = 0.0

        for opsin in self.opsins.values():
            # Absorption at this wavelength
            abs_factor = opsin.absorption_curve(np.array([wavelength_nm]))[0]
            total_response += abs_factor * opsin.conductance * intensity

        return total_response


# Example usage
def example_opsin_design():
    """Design opsins for 963 Hz and harmonics"""

    library = OpsinLibrary()

    # Target frequencies: 963 Hz fundamental, harmonics
    frequencies = [963, 1926, 2889, 3852, 4815]  # Hz

    print("Generating opsins for Arkhe frequencies:")
    library.generate_library(frequencies)

    # Test response at 963 Hz
    response = library.simulate_response(963, 1.0)
    print(f"\nTotal response at 963 Hz: {response:.3f}")

    # Plot spectra
    # opsins = list(library.opsins.values())
    # library.designer.plot_opsins(opsins)

    return library

if __name__ == "__main__":
    example_opsin_design()
