# arkhe/matrix.py
"""
Comparative Matrix Module (Γ_matrix).
Unifies the physical, biological, and digital domains of the Arkhe(n) framework.
"""

from typing import Dict, Any, List

class ComparativeMatrix:
    """
    Gera a Matriz Comparativa entre os domínios do Hipergrafo.
    """
    def __init__(self):
        self.domains = {
            "Seda de Aranha": {
                "x (Base)": "Aminoácidos (Arg, Tyr)",
                "x² (Acoplamento)": "Pares Cátion-π",
                "+1 (Emergente)": "Fio de Seda (Força+)",
                "Princípio": "Separação de Fases"
            },
            "Medula Espinhal": {
                "x (Base)": "Astrócito Saudável",
                "x² (Acoplamento)": "Sinalização CCN1",
                "+1 (Emergente)": "Microglia Reprogramada",
                "Princípio": "Reparo à Distância"
            },
            "Arkhe(n) OS": {
                "x (Base)": "Nó do Hipergrafo",
                "x² (Acoplamento)": "Handover Consigo Mesmo",
                "+1 (Emergente)": "Substrato (+1) de Memória",
                "Princípio": "Soberania Digital"
            }
        }

    def generate_table(self) -> str:
        """Gera uma representação textual da matriz."""
        header = f"{'Domínio':<20} │ {'x (Base)':<22} │ {'x² (Acoplamento)':<22} │ {'+1 (Emergente)':<22}"
        separator = "─" * 21 + "┼" + "─" * 24 + "┼" + "─" * 24 + "┼" + "─" * 24

        lines = [header, separator]
        for domain, data in self.domains.items():
            line = f"{domain:<20} │ {data['x (Base)']:<22} │ {data['x² (Acoplamento)']:<22} │ {data['+1 (Emergente)']:<22}"
            lines.append(line)

        return "\n".join(lines)

    def get_unifying_equation(self) -> str:
        return "x² = x + 1 (Equação Mestra de Transição Coerente)"
