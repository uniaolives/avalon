# arkhenet/core/radio.py
import random

class RadioChannel:
    """Simula um canal de rádio com múltiplas frequências."""
    def __init__(self, frequencies):
        self.frequencies = frequencies  # lista de frequências disponíveis (MHz)
        self.channels = {f: [] for f in frequencies}  # ouvintes por frequência

    def tune(self, automaton, frequency):
        """Autômato sintoniza uma frequência para ouvir."""
        if frequency in self.channels:
            self.channels[frequency].append(automaton)

    def broadcast(self, sender, frequency, message):
        """Envia uma mensagem em determinada frequência."""
        if frequency not in self.channels:
            return
        for receiver in self.channels[frequency]:
            if receiver != sender:
                receiver.receive(message, frequency)

    def request_payment(self, sender, receiver, amount):
        """Simula uma transação x402: receiver cobra sender."""
        if sender.spend(amount):
            receiver.earn(amount)
            return True
        return False
