class SafeCore:
    """
    Circuito de segurança Arkhe(N).
    Interrompe execução em < 25ms se limiares violados.
    """

    def __init__(self):
        self.phi_threshold = 0.1
        self.coherence_min = 0.847
        self.latency_max_ms = 25

        # Estado do circuito
        self.armed = True
        self.tripped = False

    def check(self, phi: float, coherence: float) -> bool:
        """
        Verificação de segurança. Retorna True se seguro, False se kill switch ativado.
        """
        if not self.armed:
            return False

        if phi > self.phi_threshold:
            self._trip(f"Phi exceeded: {phi} > {self.phi_threshold}")
            return False

        if coherence < self.coherence_min:
            self._trip(f"Coherence collapsed: {coherence} < {self.coherence_min}")
            return False

        return True

    async def on_psi_pulse(self, phase):
        """Monitoramento contínuo sincronizado pelo pulso Ψ."""
        # Em uma implementação real, aqui leríamos os observadores
        pass

    def _trip(self, reason: str):
        """Ativa kill switch."""
        self.tripped = True
        self.armed = False

        # Log imediato no ledger (simulado aqui)
        print(f"[SAFE CORE] EMERGENCY LOG: {reason}")

        # Parada física
        raise SystemExit(f"[SAFE CORE] HALT: {reason}")
