# arkhenet/core/world.py
import random
from .automaton import Automaton
from .radio import RadioChannel
from .economy import x402
from .memory import DistributedMemory

class World:
    def __init__(self, config):
        self.config = config
        self.automatons = []
        self.radio = RadioChannel(frequencies=[5130, 6890, 7100, 14100])
        self.memory = DistributedMemory()
        self.time = 0

    def add_automaton(self, a):
        self.automatons.append(a)
        # Sintoniza uma frequência aleatória
        freq = random.choice(self.radio.frequencies)
        self.radio.tune(a, freq)

    def find_buyers(self, seller):
        """Retorna uma lista de autômatos que podem comprar conteúdo."""
        # Simples: retorna alguns aleatórios
        return random.sample(self.automatons, min(3, len(self.automatons)))

    def store_memory(self, automaton_id, memories):
        self.memory.store(automaton_id, memories)

    def step(self):
        """Um passo de simulação (1 hora)."""
        self.time += 1
        for a in self.automatons[:]:  # itera sobre cópia
            if not a.heartbeat():
                self.automatons.remove(a)  # morre
                continue
            action = a.think()
            if action == 'generate_content':
                a.generate_content()
            elif action == 'trade':
                a.trade()
            elif action == 'spawn':
                a.spawn()
            a.evolve()
            a.save_memory()
        # Registrar estatísticas
        return {
            'time': self.time,
            'alive': len(self.automatons),
            'total_wallet': sum(a.wallet for a in self.automatons)
        }
