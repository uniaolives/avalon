# papercoder_kernel/lie/group.py
from typing import Callable, Optional, List
from papercoder_kernel.core.ast import Program
from papercoder_kernel.lie.algebra import VectorField

class Diffeomorphism:
    """Elemento do grupo de difeomorfismos (refatoração finita)."""
    def __init__(self, name: str, mapping: Callable[[Program], Program]):
        self.name = name
        self.mapping = mapping
        self.inverse: Optional['Diffeomorphism'] = None

    def __call__(self, p: Program) -> Program:
        return self.mapping(p)

    def compose(self, other: 'Diffeomorphism') -> 'Diffeomorphism':
        """Composição de difeomorfismos (multiplicação do grupo)."""
        return Diffeomorphism(
            f"{self.name}∘{other.name}",
            lambda p: self.mapping(other.mapping(p))
        )

    def set_inverse(self, inv: 'Diffeomorphism'):
        self.inverse = inv
        if inv.inverse != self:
            inv.inverse = self

class DiffeomorphismGroup:
    """Grupo de Lie de difeomorfismos."""
    def __init__(self):
        self.identity = Diffeomorphism("id", lambda p: p)
        self.identity.set_inverse(self.identity)
        self.elements: List[Diffeomorphism] = [self.identity]

    def exponential(self, v: VectorField, steps: int = 100) -> Diffeomorphism:
        """Mapa exponencial: integra um campo vetorial em um difeomorfismo."""
        def flow(p: Program) -> Program:
            current = p
            dt = 1.0 / steps
            for _ in range(steps):
                current = v.apply(current, dt)
            return current
        return Diffeomorphism(f"exp({v.name})", flow)
