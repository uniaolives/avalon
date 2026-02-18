class HIMemory:
    """
    O H I como memória persistente (ledger) do hipergrafo cósmico.
    Preserva a assinatura do meio interestelar original.
    """

    def __init__(self):
        self.components = 2
        self.velocities = [-36.3, 18.1]  # km/s
        self.fwhm = [38.2, 44.1]  # km/s
        self.column_density = [1.21e21, 1.09e21]  # cm^-2

    def compare_with_oh(self, oh_velocity: float):
        """Compara memória H I com sinal OH ativo."""
        # OH é blueshifted (~ -120 km/s) indicando outflow
        if oh_velocity < min(self.velocities) - 50:
            return "OH tracing outflow, HI tracing ambient medium"
        return "Co-spatial or complex kinematics"
