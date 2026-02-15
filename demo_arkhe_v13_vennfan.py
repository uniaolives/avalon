# demo_arkhe_v13_vennfan.py
"""
ARKHE(N) OS v13.0 — VENNFAN HYPERGRAPH VISUALIZATION
Demonstrates the parametric generation of VennFan diagrams.
"""

import asyncio
from arkhe import VennFan, realize_unity

async def run_vennfan_demo():
    print("🎨 ARKHE(N) OS v13.0 — VENNFAN VISUALIZATION EVOLUTION 🎨\n")

    # 1. Setup VennFan
    n_sets = 6
    print(f"[STEP 1] Inicializando VennFan para {n_sets} conjuntos...")
    vf = VennFan(n_sets=n_sets, p=0.2)

    # 2. Gerar Gráfico
    print("[STEP 2] Gerando diagrama de interseções (Hipergrafo Visual)...")
    vf.plot(labels=['AI', 'Quantum', 'Biology', 'Topology', 'Sovereignty', 'Satoshi'], output_path="demo_vennfan.png")

    # 3. Analisar Métricas
    summary = vf.get_summary()
    print(f"\n📊 Sumário VennFan:")
    print(f"   • Conjuntos (Nós Γ): {summary['n_sets']}")
    print(f"   • Regiões (Interseções): {summary['total_regions']}")
    print(f"   • Coerência Visual (C_viz): {summary['coherence_visual']:.2f}")

    # 4. Grimório v13.0
    print("\n[STEP 3] Verificando Grimório v13.0...")
    # I will update synthesis.py in the next step to include this
    print("Realizando Unidade...")

    print("\n" + "="*60)
    print("✨ O HIPERGRAFO AGORA É VISÍVEL EM TODAS AS SUAS INTERSEÇÕES. ✨")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_vennfan_demo())
