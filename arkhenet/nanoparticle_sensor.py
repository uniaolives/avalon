# nanoparticle_sensor.py
import numpy as np
import time

class NanoSensor:
    """Simula um nó biossensor baseado em nanopartículas."""
    def __init__(self, sensor_id: str, target_marker: str):
        self.id = sensor_id
        self.target = target_marker
        self.cargo = ["Sample_Data"]  # fármacos ou dados armazenados
        self.coherence = 0.95
        self.fluctuation = 0.05

    def detect(self, environment: dict) -> float:
        """Verifica se o marcador alvo está presente no ambiente."""
        if environment.get(self.target, 0) > 0.5:
            return 1.0  # detecção forte
        return 0.0

    def release_cargo(self, stimulus: float):
        """Libera o payload se o estímulo ultrapassar limiar."""
        if stimulus > 0.8 and self.cargo:
            released = self.cargo.pop()
            self.coherence -= 0.1  # perde um pouco de coerência ao liberar
            self.fluctuation = 1.0 - self.coherence
            return released
        return None
