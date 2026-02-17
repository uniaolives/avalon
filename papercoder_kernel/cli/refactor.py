# papercoder_kernel/cli/refactor.py
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações do pacote
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from papercoder_kernel.core.ast import parse_program
from papercoder_kernel.lie.group import DiffeomorphismGroup, Diffeomorphism
from papercoder_kernel.safety.theorem import is_safe_refactoring, perturb

def load_diffeomorphism(name: str, group: DiffeomorphismGroup) -> Diffeomorphism:
    """Carrega ou cria um difeomorfismo por nome."""
    if name == "rename":
        # Simula uma refatoração de renomeação
        return Diffeomorphism(name, lambda p: perturb(p, 0.1))
    elif name == "identity":
        return group.identity
    else:
        # Outras transformações simuladas
        return Diffeomorphism(name, lambda p: perturb(p, 0.5))

def main():
    if len(sys.argv) < 4:
        print("Uso: python -m papercoder_kernel.cli.refactor <arquivo_origem> <arquivo_destino> <refatoracao>")
        sys.exit(1)

    src_file, dst_file, ref_name = sys.argv[1:4]

    # Em um sistema real, leríamos os arquivos. Aqui simulamos.
    src = parse_program(src_file)

    # Carregar o grupo de difeomorfismos
    group = DiffeomorphismGroup()

    # Obter a refatoração selecionada
    phi = load_diffeomorphism(ref_name, group)

    # Aplicar a refatoração
    transformed = phi(src)

    print(f"Analisando refatoração '{ref_name}'...")

    if is_safe_refactoring(phi, group):
        print(f"✅ Refatoração '{ref_name}' é segura e preserva semântica.")
        # Simula salvar o resultado (transformed seria gravado em dst_file)
        # transformed.save(dst_file)
    else:
        print(f"❌ Refatoração '{ref_name}' não é segura (migração necessária).")
        sys.exit(2)

if __name__ == "__main__":
    main()
