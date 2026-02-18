# papercoder_kernel/cli/refactor.py
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações do pacote
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from papercoder_kernel.core.program_ast import parse_program, Program
from papercoder_kernel.core.ast import parse_program, Program
from papercoder_kernel.lie.group import DiffeomorphismGroup, Diffeomorphism
from papercoder_kernel.lie.algebra import VariableRenameField, FunctionExtractField
from papercoder_kernel.safety.theorem import is_safe_refactoring

def load_diffeomorphism(name: str, group: DiffeomorphismGroup) -> Diffeomorphism:
    """Carrega ou cria um difeomorfismo funcional por nome."""
    if name == "rename":
        # Exemplo real: renomear 'x' para 'y'
        v = VariableRenameField("x", "y")
        return group.exponential(v)
    elif name == "extract":
        v = FunctionExtractField("new_func", [0, 1])
        return group.exponential(v)
    elif name == "identity":
        return group.identity
    else:
        # Fallback para transformações genéricas (comentário de fluxo)
        from papercoder_kernel.safety.theorem import perturb
        return Diffeomorphism(name, lambda p: perturb(p, 0.1))

def main():
    if len(sys.argv) < 4:
        print("Uso: python -m papercoder_kernel.cli.refactor <arquivo_origem> <arquivo_destino> <refatoracao>")
        sys.exit(1)

    src_file, dst_file, ref_name = sys.argv[1:4]

    if not os.path.exists(src_file):
        print(f"Erro: Arquivo {src_file} não encontrado.")
        sys.exit(1)

    # 1. Parsing real do arquivo
    src = parse_program(src_file)

    # 2. Carregar o grupo de difeomorfismos
    group = DiffeomorphismGroup()

    # 3. Obter a refatoração funcional
    phi = load_diffeomorphism(ref_name, group)

    # 4. Aplicar a refatoração no manifold de programas
    transformed = phi(src)

    print(f"Analisando refatoração '{ref_name}' no arquivo {src_file}...")

    # 5. Validação de Prova de Preservação Semântica
    from papercoder_kernel.types.proofs import verify_semantic_preservation
    if not verify_semantic_preservation(src, transformed, phi):
        print(f"❌ Falha na prova de preservação semântica.")
        sys.exit(3)

    # 6. Validação via Teorema PaperCoder Safety
    # 5. Validação via Teorema PaperCoder Safety
    if is_safe_refactoring(phi, group):
        print(f"✅ Refatoração '{ref_name}' é segura e preserva semântica.")
        # 6. Salvar o resultado real no disco
        transformed.save(dst_file)
        print(f"🚀 Resultado gravado em {dst_file}")
    else:
        print(f"❌ Refatoração '{ref_name}' não é segura (migração necessária).")
        sys.exit(2)

if __name__ == "__main__":
    main()
