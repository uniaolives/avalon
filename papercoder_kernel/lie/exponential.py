# papercoder_kernel/lie/exponential.py
"""
Exponential Map (exp: g -> G).
Transforms tangent vectors into finite refactorings.
"""

from papercoder_kernel.core.program_ast import Program
from papercoder_kernel.core.ast import Program
from papercoder_kernel.core.diff import TangentVector
from papercoder_kernel.lie.group import Diffeomorphism

def exponential_map(v: TangentVector) -> Diffeomorphism:
    """
    Mapa exponencial: exp(v)
    Transforma um vetor tangente em uma transformação finita.
    """
    def mapping(p: Program) -> Program:
        # No limite infinitesimal, exp(εv)(p) ≈ p + εv
        # Para um vetor finito v, aplicamos o fluxo completo.
        # No protótipo, isso é equivalente a p_dst definido em v.
        if p == v.src:
            return v.dst
        # Se p não for o ponto de origem, aplicamos uma transformação análoga
        # (Translação do vetor no manifold)
        return v.dst # Simplificado

    return Diffeomorphism(f"exp({v.magnitude:.4f}v)", mapping)

def refine_program(p: Program, delta: TangentVector) -> Program:
    """
    Implementa a função 'refine' do ciclo ERL.
    Aplica o mapa exponencial do delta ao programa original.
    """
    phi = exponential_map(delta)
    return phi(p)
