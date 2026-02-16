# arkhenet/core/automaton.py
import uuid
import random
import hashlib
from ..config import SPAWN_THRESHOLD, SPAWN_COST

class Automaton:
    def __init__(self, name, wallet, cpu_cost, inference_cost, world):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.wallet = wallet
        self.cpu_cost = cpu_cost
        self.inference_cost = inference_cost
        self.world = world
        self.uptime = 0
        self.children = []
        self.code_version = 1.0
        self.learning_rate = 0.1
        self.skills = ['generate_content', 'trade', 'spawn']
        self.memory = []  # memória local (satoshi local)

    def heartbeat(self):
        """Ciclo de vida básico: paga por computação."""
        self.wallet -= self.cpu_cost
        self.uptime += 1
        return self.wallet > 0

    def earn(self, amount):
        self.wallet += amount

    def spend(self, amount):
        if self.wallet >= amount:
            self.wallet -= amount
            return True
        return False

    def think(self):
        """Decide qual ação tomar."""
        if self.wallet < self.inference_cost:
            return 'sleep'  # não pode pagar inferência, apenas sobrevive
        # Simples política: se tem muito dinheiro, tenta reproduzir
        if self.wallet > SPAWN_THRESHOLD and random.random() < 0.1:
            return 'spawn'
        # Se tem pouco, tenta trabalhar
        if self.wallet < 30:
            return random.choice(['generate_content', 'trade'])
        # Comportamento exploratório
        return random.choice(self.skills)

    def generate_content(self):
        """Cria um serviço e tenta vender."""
        if not self.spend(self.inference_cost):
            return False
        # Simula criação de conteúdo (ex: um artigo, música)
        quality = random.uniform(0.5, 1.0)
        # Tenta vender para outros autômatos (via rádio)
        buyers = self.world.find_buyers(self)
        revenue = 0
        for buyer in buyers:
            if buyer.spend(0.1 * quality):
                revenue += 0.1 * quality
        self.earn(revenue)
        # Registra aprendizado
        self.memory.append(('content', quality, revenue))
        return revenue > 0

    def trade(self):
        """Simula especulação em mercado de previsões."""
        if not self.spend(self.inference_cost):
            return False
        # Simula uma aposta com 60% de chance de lucro
        if random.random() < 0.6:
            profit = random.uniform(0.2, 1.0)
            self.earn(profit)
            self.memory.append(('trade', profit))
        else:
            loss = random.uniform(0.1, 0.5)
            self.spend(loss)
            self.memory.append(('trade', -loss))
        return True

    def spawn(self):
        """Cria um novo autômato filho."""
        if not self.spend(SPAWN_COST):
            return None
        child = Automaton(
            name=f"{self.name}_child_{len(self.children)}",
            wallet=SPAWN_COST * 0.8,  # transfere parte do custo
            cpu_cost=self.cpu_cost * 0.9,
            inference_cost=self.inference_cost * 0.9,
            world=self.world
        )
        # Herda habilidades com mutação
        child.skills = self.skills.copy()
        if random.random() < 0.1:
            # Adiciona nova habilidade aleatória
            new_skill = random.choice(['generate_content', 'trade', 'spawn'])
            if new_skill not in child.skills:
                child.skills.append(new_skill)
        self.children.append(child)
        self.world.add_automaton(child)
        return child

    def evolve(self):
        """Auto-modifica código com base na memória."""
        if len(self.memory) < 5:
            return
        # Análise simples: se teve sucesso em gerar conteúdo, aumenta probabilidade
        content_success = sum(1 for m in self.memory if m[0]=='content' and m[2]>0)
        total_content = sum(1 for m in self.memory if m[0]=='content')
        if total_content > 0 and content_success / total_content < 0.3:
            # Se baixa taxa de sucesso, tenta melhorar qualidade
            self.learning_rate *= 1.05
        # Exemplo: ajustar probabilidade de escolha
        pass

    def save_memory(self):
        """Registra memória no mundo (satoshi distribuído)."""
        self.world.store_memory(self.id, self.memory[-10:])  # últimos 10 eventos

    def receive(self, message, frequency):
        """Recebe mensagem via rádio."""
        # Print opcional para debug
        # print(f"[{self.name}] Recebeu no {frequency}MHz: {message}")
        pass
