# simulate_arkhe_ascii.py
"""
Simulação Visual do Hipergrafo Arkhe(N) via ASCII.
Utiliza o Safe Core para processar métricas e o ASCIIHypergraphRenderer para visualização.
"""

import asyncio
import numpy as np
import threading
import time
from papercoder_kernel.core.safe_core import SafeCore
from papercoder_kernel.core.ascii_runtime import ASCIIHypergraphRenderer, ASCIIOutputNode

def run_core_background(core: SafeCore):
    """Atualiza o Safe Core em segundo plano com um estado quântico dinâmico."""
    while core.is_active:
        # Simula um estado quântico oscilante
        t = time.time()
        q_state = np.random.randn(64) * (0.9 + 0.1 * np.sin(t))
        q_state = q_state / np.linalg.norm(q_state)
        core.monitor(q_state)
        time.sleep(1/40)

def main():
    print("🛡️ INICIANDO RENDERIZADOR ASCII ARKHE-N")
    time.sleep(1)

    core = SafeCore(node_id="visual_core_01")
    renderer = ASCIIHypergraphRenderer(width=80, height=24)
    output_node = ASCIIOutputNode(core, renderer)

    # Inicia processamento do core em background
    core_thread = threading.Thread(target=run_core_background, args=(core,), daemon=True)
    core_thread.start()

    # Inicia renderização (loop principal)
    output_node.run()

if __name__ == "__main__":
    main()
