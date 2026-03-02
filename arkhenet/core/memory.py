# arkhenet/core/memory.py
class DistributedMemory:
    """Memória distribuída (satoshi) da rede."""
    def __init__(self):
        self.storage = {}  # automaton_id -> lista de memórias

    def store(self, automaton_id, memories):
        if automaton_id not in self.storage:
            self.storage[automaton_id] = []
        self.storage[automaton_id].extend(memories)
        # Limitar tamanho
        if len(self.storage[automaton_id]) > 100:
            self.storage[automaton_id] = self.storage[automaton_id][-100:]

    def query(self, automaton_id):
        return self.storage.get(automaton_id, [])
