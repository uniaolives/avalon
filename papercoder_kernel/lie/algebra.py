# papercoder_kernel/lie/algebra.py
import ast
from typing import Callable, Optional, Dict, List
import numpy as np
from papercoder_kernel.core.program_ast import Program
from papercoder_kernel.core.ast import Program

class VectorField:
    """Campo vetorial no espaço de programas."""
    def __init__(self, name: str, generator: Callable[[Program, float], Program]):
        self.name = name
        self.generator = generator
        self.completeness: Optional[bool] = None

    def apply(self, p: Program, epsilon: float) -> Program:
        return self.generator(p, epsilon)

class VariableRenameTransformer(ast.NodeTransformer):
    """Transformer que renomeia variáveis."""
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name

    def visit_Name(self, node):
        if node.id == self.old_name:
            return ast.copy_location(ast.Name(id=self.new_name, ctx=node.ctx), node)
        return self.generic_visit(node)

    def visit_arg(self, node):
        if node.arg == self.old_name:
            node.arg = self.new_name
        return self.generic_visit(node)

def VariableRenameField(old_name: str, new_name: str) -> VectorField:
    """Gerador de campo vetorial para renomeação de variáveis."""
    def generator(p: Program, epsilon: float) -> Program:
        # Apenas aplica se epsilon for significativo (simulação de fluxo)
        if epsilon < 0.5:
            return p

        tree = ast.parse(p.source_code)
        transformer = VariableRenameTransformer(old_name, new_name)
        new_tree = transformer.visit(tree)
        ast.fix_missing_locations(new_tree)

        # Em Python 3.9+, ast.unparse está disponível
        if hasattr(ast, 'unparse'):
            new_source = ast.unparse(new_tree)
        else:
            # Fallback (mock) se unparse não existir
            new_source = p.source_code.replace(old_name, new_name)

        return Program(new_source, p.type_context)

    return VectorField(f"rename({old_name}->{new_name})", generator)

def FunctionExtractField(func_name: str, body_indices: List[int]) -> VectorField:
    """Gerador de campo vetorial para extração de função (stub funcional)."""
    def generator(p: Program, epsilon: float) -> Program:
        if epsilon < 0.5:
            return p

        # Para simplificar o protótipo real, apenas adicionamos um marcador
        # Em um sistema completo, moveríamos nós da AST para uma nova FunctionDef
        new_source = f"{p.source_code}\ndef {func_name}(): pass # extracted"
        return Program(new_source, p.type_context)

    return VectorField(f"extract({func_name})", generator)
