# reflexo_arkhe.py
# Ciclo completo de estímulo-resposta no hipergrafo vivo

import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import time

# --- Camada Molecular (Lipídios) ---
@dataclass
class LipidNode:
    pi_type: str
    concentration: float

class PlasmaMembrane:
    def __init__(self):
        self.pis = {
            'PI': LipidNode('PI', 100),
            'PI4P': LipidNode('PI4P', 30),
            'PI45P2': LipidNode('PI(4,5)P2', 50),
            'PI345P3': LipidNode('PI(3,4,5)P3', 5)
        }
        self.kinases = {
            'PI3K': {'substrate': 'PI45P2', 'product': 'PI345P3'},
            'PIP5K': {'substrate': 'PI4P', 'product': 'PI45P2'}
        }
        self.phosphatases = {
            'PTEN': {'substrate': 'PI345P3', 'product': 'PI45P2'}
        }
        self.receptors = ['GPCR', 'RTK']  # receptores simulados

    def stimulate_receptor(self, receptor_type: str, intensity: float):
        """Estímulo externo ativa receptor, que ativa PI3K"""
        print(f"⚡ Estímulo em receptor {receptor_type} (intensidade {intensity})")
        if receptor_type in self.receptors:
            # Ativa PI3K proporcionalmente à intensidade
            self._activate_kinase('PI3K', intensity)
            return True
        return False

    def _activate_kinase(self, kinase: str, intensity: float):
        if kinase not in self.kinases:
            return
        sub = self.kinases[kinase]['substrate']
        prod = self.kinases[kinase]['product']
        # Converte substrato em produto, limitado pela disponibilidade
        amount = min(self.pis[sub].concentration, intensity * 10)
        self.pis[sub].concentration -= amount
        self.pis[prod].concentration += amount
        print(f"   → Handover lipídico: {amount:.1f} {sub} → {prod}")

# --- Camada Iônica (Canais) ---
class IonChannel:
    def __init__(self, name, pi_sensor, conductance):
        self.name = name
        self.pi_sensor = pi_sensor  # tipo de PI que modula
        self.conductance = conductance
        self.open_prob = 0.0

    def sense_pi(self, pi_concentration):
        """Abre o canal baseado na concentração do PI sensor"""
        # Modelo simples: probabilidade de abertura proporcional ao PI
        self.open_prob = min(1.0, pi_concentration / 100)
        return self.open_prob

# --- Camada Neural (HDC simplificado) ---
class NeuralNode:
    def __init__(self, layer: str, threshold: float):
        self.layer = layer  # 'sensorial', 'associativo', 'motor'
        self.threshold = threshold
        self.potential = 0.0

    def receive_current(self, current):
        self.potential += current
        if self.potential >= self.threshold:
            self.fire()
            return True
        return False

    def fire(self):
        print(f"   🔥 Neurônio {self.layer} disparou!")
        self.potential = 0.0

class HDCModel:
    def __init__(self):
        # Cadeia hierárquica simples
        self.sensory = NeuralNode('sensorial', 0.5)
        self.associative = NeuralNode('associativo', 0.7)
        self.motor = NeuralNode('motor', 0.6)

    def process(self, input_current):
        if self.sensory.receive_current(input_current):
            # Propaga para associativo
            if self.associative.receive_current(0.3):
                # Propaga para motor
                self.motor.receive_current(0.4)

# --- Camada de Resposta (Vesículas) ---
class Golgi:
    def __init__(self):
        self.vesicles = {'cargo_A': 10, 'cargo_B': 5}

    def release_vesicle(self, cargo_type: str, target: str):
        if self.vesicles.get(cargo_type, 0) > 0:
            self.vesicles[cargo_type] -= 1
            print(f"📦 Vesícula com {cargo_type} liberada para {target}")
            return True
        return False

# --- Sistema de Reflexo Integrado ---
class ArkheReflex:
    def __init__(self):
        self.membrane = PlasmaMembrane()
        self.channels = [
            IonChannel('Kv1.1', 'PI45P2', 10),
            IonChannel('Kv1.2', 'PI45P2', 8)
        ]
        self.hdc = HDCModel()
        self.golgi = Golgi()

    def stimulus(self, receptor: str, intensity: float):
        """Ponto de entrada do estímulo"""
        print("\n🔵 INÍCIO DO REFLEXO")
        # 1. Ativa receptor → handover lipídico
        self.membrane.stimulate_receptor(receptor, intensity)

        # 2. Canais iônicos sentem novo perfil lipídico
        pi45p2_conc = self.membrane.pis['PI45P2'].concentration
        for ch in self.channels:
            prob = ch.sense_pi(pi45p2_conc)
            print(f"   Canal {ch.name}: prob. abertura = {prob:.2f}")
            # Corrente proporcional à probabilidade (simplificado)
            if prob > 0.5:
                # Gera corrente de entrada no neurônio sensorial
                self.hdc.sensory.receive_current(prob * 0.5)

        # 3. Processamento HDC
        print("   🧠 Processamento neural...")
        self.hdc.process(0)  # já passamos correntes

        # 4. Resposta motora: se motor disparou, libera vesícula
        if self.hdc.motor.potential >= self.hdc.motor.threshold:
            self.golgi.release_vesicle('cargo_A', 'membrana')
            print("✅ RESPOSTA: movimento/liberação concluída")
        else:
            print("⏳ Nenhuma resposta motora gerada")

        print("🔴 FIM DO REFLEXO\n")

if __name__ == "__main__":
    # Simular
    reflexo = ArkheReflex()
    reflexo.stimulus('RTK', intensity=0.8)
