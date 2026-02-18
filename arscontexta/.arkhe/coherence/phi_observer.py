class PhiObserver:
    """Calcula Φ via entropia de emaranhamento."""
    def __init__(self, psi_cycle=None):
        self.psi = psi_cycle
        self.current_phi = 0.0
        if self.psi:
            self.psi.subscribe(self)

    async def on_psi_pulse(self, phase):
        # Simulação de cálculo de Phi
        self.current_phi = 0.006 + (phase % 10) * 0.001

    def get_phi(self):
        return self.current_phi
