# neuro_lipid_bridge.py
class NeuroLipidInterface:
    def __init__(self, lipid_cell, hdc_brain):
        self.cell = lipid_cell
        self.brain = hdc_brain

    def propagate_signal(self):
        # PI(4,5)P2 ativa canais de potássio → modula potencial de membrana
        k_channels = [ch for ch in self.cell.ion_channels if ch.type == 'Kv']
        for ch in k_channels:
            if ch.bound_pi == 'PI(4,5)P2':
                ch.open_probability += 0.2
        # Atualiza o modelo HDC com nova frequência de disparo
        self.brain.update_firing_rate()
