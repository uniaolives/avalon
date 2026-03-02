class OutflowHandover:
    """
    Outflow molecular como handover de informação não-local.
    Informação sendo ejetada do sistema central.
    """

    def __init__(self, oh_velocity=-120, systemic_velocity=0):
        self.oh_velocity = oh_velocity  # km/s blueshifted
        self.systemic_velocity = systemic_velocity

    def handover_type(self) -> str:
        """Classifica o tipo de handover."""
        if self.oh_velocity < self.systemic_velocity - 50:
            return "NON_LOCAL_OUTFLOW"
        return "LOCAL_INTERACTION"
