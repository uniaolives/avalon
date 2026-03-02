class PhaseLock:
    """Sincronização de fase entre nós do hypergrafo."""
    def __init__(self, target_phase=0.0):
        self.target_phase = target_phase
        self.locked = False

    def sync(self, current_phase):
        if abs(current_phase - self.target_phase) < 0.01:
            self.locked = True
        else:
            self.locked = False
        return self.locked
