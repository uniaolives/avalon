# disease_models.py – Simulação de perturbações
class DiseaseHypergraph:
    def __init__(self, healthy_cell):
        self.cell = healthy_cell

    def cancer_mutation(self):
        # Simula perda de PTEN
        for pm in self.cell.membranes['plasma'].phosphatases:
            if pm.enzyme_name == 'PTEN':
                pm.active = False
        print("⚠️ PTEN inativado – sinal de sobrevivência constitutivo")

    def alzheimer_dysfunction(self):
        # Reduz PI(4,5)P2 disponível
        pm = self.cell.membranes['plasma']
        for pi in pm.pis:
            if pi.pi_type == 'PI(4,5)P2':
                pi.concentration *= 0.3
        print("⚠️ PI(4,5)P2 reduzido – clivagem de APP alterada")
