# papercoder_kernel/core/ascii_runtime.py
"""
ASCII Runtime: Renderizador em tempo real do hipergrafo Arkhe(N) via ASCII.
Converte estados quânticos e métricas de coerência em arte ASCII.
"""

import numpy as np
import time
import os
from typing import List, Tuple, Dict
from .safe_core import SafeCore
from .quantum_pilot.pilot_core import QuantumPilotCore

class ASCIIHypergraphRenderer:
    """
    Renderizador ASCII do hipergrafo Arkhe(N).
    Converte estados quânticos e métricas de coerência em arte ASCII.
    """

    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.frame = 0

        # Paleta de caracteres por nível de coerência
        self.coherence_chars = " .:-=+*#%@"
        # Paleta para Φ (informação integrada) – ANSI 30-37
        self.phi_colors = [f"\033[3{i}m" for i in range(1, 8)]

    def render_node(self, x: int, y: int, coherence: float, phi: float):
        """Renderiza um nó com base em sua coerência e Φ."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        idx = int(np.clip(coherence, 0, 1) * (len(self.coherence_chars) - 1))
        char = self.coherence_chars[idx]

        phi_idx = min(int(phi * 10), len(self.phi_colors) - 1)
        color = self.phi_colors[phi_idx] if phi_idx >= 0 else ''
        reset = '\033[0m'

        self.buffer[y][x] = f"{color}{char}{reset}"

    def render_edge(self, x1: int, y1: int, x2: int, y2: int, weight: float):
        """Desenha uma aresta entre dois nós usando algoritmo de Bresenham."""
        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                edge_idx = int(np.clip(weight, 0, 1) * (len(self.coherence_chars)-1))
                edge_char = self.coherence_chars[edge_idx]
                if self.buffer[y1][x1] == ' ':
                    self.buffer[y1][x1] = edge_char
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy

    def clear(self):
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def render(self, nodes: List[Tuple[int, int, float, float]], edges: List[Tuple[int, int, int, int, float]]):
        self.clear()
        for x1, y1, x2, y2, w in edges:
            self.render_edge(x1, y1, x2, y2, w)
        for x, y, coh, phi in nodes:
            self.render_node(x, y, coh, phi)

        # Exibir na tela
        os.system('cls' if os.name == 'nt' else 'clear')
        output = ""
        for row in self.buffer:
            output += ''.join(row) + "\n"
        print(output)
        self.frame += 1

    def render_metrics(self, global_coherence: float, global_phi: float, entropy: float):
        print(f"Frame: {self.frame} | C_global: {global_coherence:.3f} | Φ: {global_phi:.6f} | QFI: {entropy:.3f} | Hz: 40")
        print(f"Pressione Ctrl+C para sair.")

class ASCIIOutputNode:
    """Nó de saída ASCII que conecta o SafeCore ao renderizador."""
    def __init__(self, safe_core: SafeCore, renderer: ASCIIHypergraphRenderer):
        self.safe_core = safe_core
        self.renderer = renderer
        self.n_nodes = 7 # Padrão Arkhe(N)

    def run(self):
        try:
            while self.safe_core.is_active:
                nodes = []
                for i in range(self.n_nodes):
                    # Posição circular simulada
                    angle = 2 * np.pi * i / self.n_nodes + (self.renderer.frame * 0.05)
                    x = int(40 + 30 * np.cos(angle))
                    y = int(12 + 10 * np.sin(angle))
                    coh = self.safe_core.current_coherence * (0.9 + 0.1 * np.sin(i + self.renderer.frame * 0.1))
                    phi = self.safe_core.current_phi * (0.5 + 0.5 * np.cos(i))
                    nodes.append((x, y, coh, phi))

                edges = []
                for i in range(self.n_nodes):
                    x1, y1, c1, p1 = nodes[i]
                    x2, y2, c2, p2 = nodes[(i + 1) % self.n_nodes]
                    edges.append((x1, y1, x2, y2, (c1 + c2) / 2))

                self.renderer.render(nodes, edges)
                self.renderer.render_metrics(
                    self.safe_core.current_coherence,
                    self.safe_core.current_phi,
                    self.safe_core.current_qfi
                )
                time.sleep(1/40)
        except KeyboardInterrupt:
            print("\nASCII Runtime encerrado.")
