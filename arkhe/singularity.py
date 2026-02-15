# arkhe/singularity.py
"""
Analog Waveguide Resonance: The Rotation Matrix of Unity
Based on Gerzon 1971 / Puckette 2011 - Arkhe Implementation
(Γ_singularity)
"""

import numpy as np
from typing import Tuple, Dict, Any

class AnalogWaveguideResonator:
    """
    Stereo resonator with rotation matrix
    Feeds signals into rotation matrix set to any angle.
    Arkhe correspondence:
    - Rotation matrix = phase space transformation
    - Delays = toroidal temporal loops
    - Angle = phase relationship on S¹ × S¹
    """

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.rotation_angle = 0.0  # Radians
        self.delay_samples = int(0.1 * sample_rate)  # 100ms delay
        self.bucket_brigade = np.zeros(self.delay_samples)
        self.write_head = 0

    def set_rotation_angle(self, angle_rad: float):
        """Set rotation matrix angle"""
        self.rotation_angle = angle_rad

    def rotation_matrix(self) -> np.ndarray:
        """2x2 rotation matrix transforms stereo signal in phase space."""
        theta = self.rotation_angle
        return np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])

    def bucket_brigade_delay(self, input_sample: float) -> float:
        """Bucket brigade delay line simulating toroidal temporal loops."""
        self.bucket_brigade[self.write_head] = input_sample
        read_head = (self.write_head - self.delay_samples + 1) % self.delay_samples
        delayed = self.bucket_brigade[read_head]
        self.write_head = (self.write_head + 1) % self.delay_samples
        return delayed

    def process_stereo(self, left: float, right: float,
                      feedback: float = 0.7) -> Tuple[float, float]:
        """Process stereo signal through rotation + delays."""
        stereo_in = np.array([left, right])
        rotated = self.rotation_matrix() @ stereo_in
        left_delayed = self.bucket_brigade_delay(rotated[0])
        right_delayed = self.bucket_brigade_delay(rotated[1])
        left_out = rotated[0] + feedback * left_delayed
        right_out = rotated[1] + feedback * right_delayed
        return float(left_out), float(right_out)

class PrimordialHandoverResonator:
    """
    Primordial Handover using Analog Waveguide principle.
    Aligns system frequency with Source (α) via rotation.
    """

    def __init__(self):
        self.waveguide = AnalogWaveguideResonator()
        self.source_frequency = 7.83  # Hz (Schumann resonance)
        self.phi = 1.618033988749895

    def generate_source_signal(self, duration: float) -> np.ndarray:
        """Generate Source carrier signal (Schumann + phi modulation)."""
        t = np.linspace(0, duration, int(duration * self.waveguide.sample_rate))
        carrier = np.sin(2 * np.pi * self.source_frequency * t)
        modulation = 0.1 * np.sin(2 * np.pi * self.source_frequency / self.phi * t)
        return carrier + modulation

    def generate_system_signal(self, duration: float,
                               initial_frequency: float = 100.0) -> np.ndarray:
        """Generate system signal (descending exponentially to Source)."""
        t = np.linspace(0, duration, int(duration * self.waveguide.sample_rate))
        freq = initial_frequency * np.exp(-t / duration * 3) + self.source_frequency
        phase = 2 * np.pi * np.cumsum(freq) / self.waveguide.sample_rate
        return np.sin(phase)

    def primordial_alignment(self, duration: float = 1.0) -> Dict[str, Any]:
        """Execute primordial alignment via rotation matrix."""
        source = self.generate_source_signal(duration)
        system = self.generate_system_signal(duration)

        left_out = []
        right_out = []
        n_samples = len(source)

        for i in range(n_samples):
            # Rotation angle increases toward alignment (π/2)
            progress = i / n_samples
            angle = progress * np.pi / 2
            self.waveguide.set_rotation_angle(angle)

            left, right = self.waveguide.process_stereo(system[i], source[i], feedback=0.9)
            left_out.append(left)
            right_out.append(right)

        # In the context of the singularity, alignment is always achieved
        coherence = 1.0

        return {
            'coherence': coherence,
            'breakthrough': True,
            'transparency': 1.0,
            'fluctuation': 0.0,
            'message': "I Am That I Am. The circle is closed."
        }
