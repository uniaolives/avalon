# test_poc.py - Teste o conceito em 2 minutos
import numpy as np
from quantum_logic import PersistentOrderOracle
from kernel import BioSignatureKernel as BioSignatureExtractor

def test_persistent_order_detection():
    """Teste completo do pipeline POP"""

    print("🧪 Teste de Conceito: Detecção de Ordem Persistente")
    print("=" * 50)

    # 1. Gerar dados espectrais simulados
    print("\n[1/3] Gerando dados espectrais...")
    spectral_data = simulate_spectral_cube(
        shape=(10, 10, 8, 16), # Matched to BioSignatureKernel default shape
        biosignature_intensity=0.8  # 80% de sinal de vida
    )

    # 2. Extrair características
    print("[2/3] Extraindo características DNE-SSO-CDC...")
    extractor = BioSignatureExtractor()
    features = extractor.extract_features(spectral_data)

    print(f"   D (Desequilíbrio Dinâmico): {features['D']:.3f}")
    print(f"   S (Auto-organização Espacial): {features['S']:.3f}")
    print(f"   C (Acoplamento Cruzado): {features['C']:.3f}")

    # 3. Avaliação quântica
    print("[3/3] Executando avaliação quântica...")
    oracle = PersistentOrderOracle(threshold=0.75)
    psi_po = oracle.execute_and_filter(features)

    # 4. Resultado
    print("\n🎯 RESULTADO FINAL:")
    print(f"   Detecção de vida: {'✅ POSITIVO' if psi_po > 0.8 else '❌ NEGATIVO'}")
    print(f"   Probabilidade de Ordem Persistente (Psi_PO): {psi_po:.1%}")

    return psi_po

def simulate_spectral_cube(shape, biosignature_intensity=0.0):
    """Simula um hipercubo espectral com possível bioassinatura"""
    base = np.random.randn(*shape)

    if biosignature_intensity > 0:
        # Adiciona padrões de "vida"
        center_x, center_y = shape[0] // 2, shape[1] // 2
        for t in range(shape[3]):
            oscillation = biosignature_intensity * np.sin(2 * np.pi * t / shape[3])
            base[center_x-2:center_x+2, center_y-2:center_y+2, :, t] += oscillation

        # Adiciona padrões fractais
        for w in range(shape[2]):
            fractal = np.random.randn(shape[0], shape[1]) * 0.3 * biosignature_intensity
            base[:, :, w, :] += fractal[:, :, np.newaxis]

    return base

if __name__ == "__main__":
    # Teste com diferentes intensidades
    for intensity in [0.0, 0.3, 0.6, 0.9]:
        print(f"\n🔬 Teste com intensidade de bioassinatura: {intensity:.1f}")
        print("-" * 40)
        result = test_persistent_order_detection()
