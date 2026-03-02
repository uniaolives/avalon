# test_erl_integration.py
import unittest
import torch
from papercoder_kernel.core.program_ast import Program
from papercoder_kernel.core.ast import Program
from papercoder_kernel.core.self_node import SelfNode
from papercoder_kernel.core.flow import ExperientialLearning

class MockEnvironment:
    def evaluate(self, y):
        # Simulação de avaliação: reward aumenta se houver comentário de eps
        if "# eps=" in y.source_code:
            return "Good", 0.8
        return "Bad", 0.2

class MockMemory:
    def __init__(self):
        self.data = []
    def store(self, delta):
        self.data.append(delta)

class TestERLIntegration(unittest.TestCase):
    def test_erl_cycle(self):
        self_node = SelfNode()
        memory = MockMemory()
        env = MockEnvironment()
        erl = ExperientialLearning(self_node, memory, env, threshold=0.5)

        x = Program("def test(): pass")
        result = erl.episode(x)

        self.assertIn('final_program', result)
        self.assertIsInstance(result['final_program'], Program)
        # Se a primeira tentativa falhar (eps < 0.1), o refinamento deve ocorrer
        print(f"Final Program Source: {result['final_program'].source_code}")

if __name__ == "__main__":
    unittest.main()
