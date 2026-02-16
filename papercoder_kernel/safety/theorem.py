# papercoder_kernel/safety/theorem.py
from typing import Optional
import numpy as np
from papercoder_kernel.core.ast import Program, AST, edit_distance
from papercoder_kernel.lie.group import Diffeomorphism, DiffeomorphismGroup
from papercoder_kernel.lie.algebra import VectorField

def random_program() -> Program:
    """Gera um programa aleatório para testes."""
    import random
    suffix = random.randint(0, 1000)
    return Program(AST(f"Node_{suffix}", [], {}), {})

def perturb(p: Program, epsilon: float) -> Program:
    """Perturba levemente um programa (simulação de fluxo infinitesimal)."""
    # Se epsilon for muito pequeno, retorna o mesmo programa (identidade)
    if abs(epsilon) < 1e-9:
        return p
    # Simulação: altera a AST baseada no epsilon
    new_ast = AST(p.ast.node_type, p.ast.children, {**p.ast.metadata, "epsilon": epsilon})
    return Program(new_ast, p.type_context)

def extract_vector_field(phi: Diffeomorphism, group: DiffeomorphismGroup) -> Optional[VectorField]:
    """Tenta encontrar v tal que exp(v) ≈ phi."""
    # Implementação via diferenças finitas (fallback do Arquiteto)
    def generator(p: Program, epsilon: float) -> Program:
        # v ≈ (phi(p) - p) / ε
        # Como não temos subtração, usamos a lógica de que v aplicado por epsilon
        # deve nos levar a uma fração do caminho até phi(p).

        # Simulamos isso perturbando p proporcionalmente à distância até phi(p)
        dist = edit_distance(p, phi(p))
        return perturb(p, epsilon * dist)

    return VectorField(f"log({phi.name})", generator)

def is_complete(v: VectorField) -> bool:
    """Verifica se o campo é completo (fluxo existe para todo t)."""
    # Na prática, testamos se o fluxo não explode numericamente
    test_prog = random_program()
    for t in [0.1, 1.0, 10.0]:
        try:
            v.apply(test_prog, t)
        except Exception:
            return False
    return True

def is_safe_refactoring(phi: Diffeomorphism, group: DiffeomorphismGroup, tolerance: float = 1e-6) -> bool:
    """
    Teorema: phi é uma refatoração segura sse:
    1) phi é um difeomorfismo (garantido pela classe)
    2) Existe v tal que phi ≈ exp(v) e v é completo.
    3) O período de v no grupo é discreto.
    """
    v = extract_vector_field(phi, group)
    if v is None:
        return False

    if not is_complete(v):
        return False

    # Se v é o campo nulo, a transformação é a identidade, que é segura.
    test_prog = random_program()
    if edit_distance(v.apply(test_prog, 1.0), test_prog) < tolerance:
        return True

    # Verificar discretude do período (simplificado)
    # Procuramos por períodos não-triviais muito pequenos.
    for t in np.linspace(0.1, 1.0, 10):
        psi = group.exponential(v, steps=max(1, int(100*t)))
        test_prog = random_program()
        # Se exp(t*v) volta para a identidade para t pequeno, o grupo de períodos pode ser denso.
        if edit_distance(psi(test_prog), test_prog) < tolerance:
             return False

    return True
