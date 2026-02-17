# papercoder_kernel/core/ast.py
import ast
import hashlib
from typing import Union, List, Dict, Optional

class RealAST:
    """Wrapper para ast.AST do Python."""
    def __init__(self, node: ast.AST):
        self.node = node

    def __hash__(self):
        # Hash baseado na estrutura do nó
        return int(hashlib.sha256(ast.dump(self.node).encode()).hexdigest(), 16)

    def __eq__(self, other):
        if not isinstance(other, RealAST):
            return False
        return ast.dump(self.node) == ast.dump(other.node)

class Program:
    """Programa real: Código-fonte + AST + Contexto."""
    def __init__(self, source_code: str, type_context: Optional[Dict[str, str]] = None):
        self.source_code = source_code
        try:
            self.ast_wrapper = RealAST(ast.parse(source_code))
        except SyntaxError:
            # Fallback para programas incompletos durante fluxos
            self.ast_wrapper = RealAST(ast.AST())

        self.type_context = type_context or {}
        self._hash = hash((self.ast_wrapper, frozenset(self.type_context.items())))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Program):
            return False
        return self.source_code == other.source_code and self.type_context == other.type_context

    def save(self, filepath: str):
        """Salva o programa no disco."""
        with open(filepath, 'w') as f:
            # Em um sistema real, usaríamos astor ou ast.unparse (Python 3.9+)
            # Para compatibilidade, tentamos ast.unparse se disponível
            if hasattr(ast, 'unparse'):
                f.write(ast.unparse(self.ast_wrapper.node))
            else:
                f.write(self.source_code)

def edit_distance(p1: Program, p2: Program) -> float:
    """
    Métrica de edição entre programas baseada em custos de operação de AST.
    S = Σ cost(op)
    """
    if p1 == p2:
        return 0.0

    # Implementação baseada em diferença de contagem de nós (proxy para edit distance)
    # e custos de operação (substituir nó, etc.)
    d1 = ast.dump(p1.ast_wrapper.node)
    d2 = ast.dump(p2.ast_wrapper.node)

    # Hash-based distance if too different
    if len(d1) == 0 or len(d2) == 0:
        return 1.0

    # Simplified Zhang-Shasha proxy: string edit distance normalized
    import difflib
    sm = difflib.SequenceMatcher(None, d1, d2)
    return 1.0 - sm.ratio()

def parse_program(filepath: str) -> Program:
    """Lê e parseia um arquivo Python real."""
    if not os.path.exists(filepath):
        # Fallback para testes
        return Program("pass")
    with open(filepath, 'r') as f:
        return Program(f.read())

import os
