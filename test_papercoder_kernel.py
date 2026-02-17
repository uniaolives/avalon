# test_papercoder_kernel.py
import unittest
from papercoder_kernel.core.ast import Program, edit_distance
from papercoder_kernel.lie.algebra import VectorField
from papercoder_kernel.lie.group import Diffeomorphism, DiffeomorphismGroup
from papercoder_kernel.types.dependent import Refactor
from papercoder_kernel.safety.theorem import is_safe_refactoring, perturb, random_program

class TestPaperCoderKernel(unittest.TestCase):
    def test_core_ast(self):
        p1 = Program("def x(): pass", {"x": "int"})
        p2 = Program("def x(): pass", {"x": "int"})
        self.assertEqual(edit_distance(p1, p2), 0.0)

        p3 = Program("def x(): return 1", {})
        self.assertGreater(edit_distance(p1, p3), 0.0)

    def test_lie_algebra(self):
        p1 = random_program()
        v = VectorField("test_v", lambda p, eps: perturb(p, eps))
        p_new = v.apply(p1, 0.1)
        self.assertIsInstance(p_new, Program)
        self.assertNotEqual(p1, p_new)

    def test_lie_group(self):
        p1 = random_program()
        phi1 = Diffeomorphism("phi1", lambda p: perturb(p, 0.1))
        phi2 = Diffeomorphism("phi2", lambda p: perturb(p, 0.2))
        phi12 = phi1.compose(phi2)

        self.assertEqual(phi12(p1), phi1(phi2(p1)))

    def test_dependent_types(self):
        p_a = random_program()
        p_b = perturb(p_a, 0.1)
        p_c = perturb(p_b, 0.2)

        r1 = Refactor(p_a, p_b, lambda x: perturb(x, 0.1), lambda: True)
        r2 = Refactor(p_b, p_c, lambda x: perturb(x, 0.2), lambda: True)

        r12 = r1.compose(r2)
        self.assertEqual(r12.src, p_a)
        self.assertEqual(r12.dst, p_c)
        self.assertTrue(r12.proof())

    def test_safety_theorem(self):
        group = DiffeomorphismGroup()

        # Identidade deve ser segura
        phi_id = group.identity
        self.assertTrue(is_safe_refactoring(phi_id, group))

        # Uma pequena perturbação deve ser segura
        phi_safe = Diffeomorphism("safe", lambda p: perturb(p, 0.01))
        self.assertTrue(is_safe_refactoring(phi_safe, group))

    def test_cli_execution(self):
        import subprocess
        # Cria um arquivo de teste
        with open("src_test.py", "w") as f:
            f.write("print('hello')")

        result = subprocess.run(
            ["python3", "-m", "papercoder_kernel.cli.refactor", "src_test.py", "dst_test.py", "rename"],
            capture_output=True, text=True
        )
        self.assertIn("Refatoração 'rename' é segura", result.stdout)

if __name__ == "__main__":
    unittest.main()
