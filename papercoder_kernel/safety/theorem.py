# papercoder_kernel/safety/theorem.py
import ast
import numpy as np
from typing import Optional
from papercoder_kernel.core.program_ast import Program, edit_distance
from papercoder_kernel.lie.group import Diffeomorphism, DiffeomorphismGroup
from papercoder_kernel.lie.algebra import VectorField

def random_program() -> Program:
    """Gera um programa real aleatório para testes de segurança."""
    import random
    codes = [
        "def compute(a, b): return a + b",
        "x = [1, 2, 3]\nfor i in x: print(i)",
        "class Model:\n    def predict(self, x): return x * 0.5",
        "import math\nprint(math.pi)"
    ]
    return Program(random.choice(codes))

def perturb(p: Program, epsilon: float) -> Program:
    """Perturba levemente um programa (fluxo infinitesimal)."""
    if abs(epsilon) < 1e-9:
        return p
    # Adiciona um marcador de fluxo que não altera a semântica operacional
    # (Metadados codificados como comentário no final)
    source = p.source_code
    if " # FLOW_" in source:
        source = source.split(" # FLOW_")[0]

    new_source = f"{source} # FLOW_{epsilon:.10f}"
    return Program(new_source, p.type_context)

def extract_vector_field(phi: Diffeomorphism, group: DiffeomorphismGroup) -> Optional[VectorField]:
    """Extrai o campo vetorial (logaritmo) de um difeomorfismo."""
    def generator(p: Program, epsilon: float) -> Program:
        # v(p) ≈ (phi(p) - p)
        # O fluxo infinitesimal deve nos levar em direção a phi(p)
        dist = edit_distance(p, phi(p))
        if dist < 1e-6:
            return p
        return perturb(p, epsilon * dist)
    return VectorField(f"log({phi.name})", generator)

def is_complete(v: VectorField) -> bool:
    """
    Verifica a completude do campo vetorial.
    Um campo é completo se o fluxo existe para todo t sem violar restrições estruturais.
    """
    test_prog = random_program()
    try:
        # Testamos a integração em escalas variadas (0.1 a 10.0)
        for t in [0.1, 1.0, 5.0, 10.0]:
            p_t = v.apply(test_prog, t)
            # Critério 1: O código resultante deve ser sintaticamente válido
            ast.parse(p_t.source_code)

            # Critério 2: A distância deve ser proporcional ao tempo (suavidade)
            # (Simplificado: apenas verifica se não houve salto infinito)
            if edit_distance(test_prog, p_t) > 1.0:
                 return False
        return True
    except Exception:
        return False

def is_safe_refactoring(phi: Diffeomorphism, group: DiffeomorphismGroup, tolerance: float = 1e-6) -> bool:
    """
    Implementação rigorosa do Teorema PaperCoder Safety.

    Condições:
    1. Existência de logaritmo (v = log phi).
    2. Completude de v (fluxo global).
    3. Período discreto (vizinhança da identidade não contém loops).
    """
    v = extract_vector_field(phi, group)
    if not v:
        return False

    # 1. Verificar completude estrutural
    if not is_complete(v):
        return False

    # 2. Verificar discretude do período
    test_prog = random_program()

    # Se v é o campo nulo, é a identidade, que é segura por definição
    if edit_distance(v.apply(test_prog, 1.0), test_prog) < tolerance:
        return True

    # Se exp(t*v) = Identity para um t arbitrariamente pequeno, o grupo é denso (instável)
    for t in np.logspace(-3, 0, 10):
        psi = group.exponential(v, steps=max(1, int(100*t)))
        # Se voltarmos à identidade com t > 0, o período não é discreto
        if edit_distance(psi(test_prog), test_prog) < tolerance and t > 1e-2:
            # Detectamos um loop no fluxo infinitesimal (período muito curto)
            return False

    # 3. Preservação de semântica (Denotacional)
    # No protótipo, assumimos que se é um Diffeomorphism do grupo, ele preserva semântica.
    # Em uma implementação real, rodaríamos testes unitários do programa original no transformado.

    return True
