# whole_cell.py
class Organelle:
    def __init__(self, name, pi_code):
        self.name = name
        self.pis = pi_code  # dict: PI_type -> count
        self.handovers = []  # conexões com outras organelas

class CellHypergraph:
    def __init__(self):
        self.organelles = {}
        self.create_organelles()

    def create_organelles(self):
        self.organelles['plasma'] = Organelle('plasma', {'PI(4,5)P2': 100, 'PI': 50})
        self.organelles['endosome'] = Organelle('endosome', {'PI(3)P': 80})
        self.organelles['golgi'] = Organelle('golgi', {'PI(4)P': 60})
        self.organelles['ER'] = Organelle('ER', {'PI': 200})

    def vesicle_handover(self, from_org, to_org, pi_type, amount):
        if from_org.pis[pi_type] >= amount:
            from_org.pis[pi_type] -= amount
            to_org.pis[pi_type] = to_org.pis.get(pi_type, 0) + amount
            print(f"Handover: {amount}x {pi_type} de {from_org.name} para {to_org.name}")
