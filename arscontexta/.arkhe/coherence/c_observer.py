class CObserver:
    """Mede coerência global C(t)."""
    def __init__(self, psi_cycle=None):
        self.psi = psi_cycle
        self.current_c = 1.0
        if self.psi:
            self.psi.subscribe(self)

    async def on_psi_pulse(self, phase):
        # Simulação de medição de Coerência
        self.current_c = 0.95 - (phase % 5) * 0.002

    def get_coherence(self):
        return self.current_c
