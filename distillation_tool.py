# distillation_tool.py
# Implementação do Algoritmo de Destilação Baseado em Arkhe(n) Language (ANL)

class DistillationAlgorithm:
    """
    Guia o processo de transformar um sistema real em uma especificação formal ANL.
    Seguindo os 7 passos definidos.
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self.steps = {
            1: "Definir Fronteiras e Escopo",
            2: "Identificar Entidades Fundamentais (Nós)",
            3: "Identificar Interações (Handovers)",
            4: "Definir Atributos",
            5: "Especificar Dinâmicas",
            6: "Definir Restrições",
            7: "Validar e Iterar"
        }
        self.model = {
            "name": system_name,
            "scope": "",
            "nodes": {},
            "handovers": [],
            "constraints": []
        }

    def run_step(self, step_num, data):
        if step_num == 1:
            self.model["scope"] = data
        elif step_num == 2:
            for n in data:
                self.model["nodes"][n["id"]] = {"description": n["desc"], "attr": [], "dynamics": ""}
        elif step_num == 3:
            self.model["handovers"].extend(data)
        elif step_num == 4:
            for node_id, attrs in data.items():
                self.model["nodes"][node_id]["attr"] = attrs
        elif step_num == 5:
            for node_id, dyn in data.items():
                self.model["nodes"][node_id]["dynamics"] = dyn
        elif step_num == 6:
            self.model["constraints"] = data
        return self

    def export_anl(self):
        """Gera um arquivo .arkhe a partir da destilação."""
        lines = [f"# {self.system_name} - Distilled ANL Model", ""]
        lines.append(f"hypergraph = Hypergraph('{self.system_name}')")
        lines.append("")

        # Handovers e Nodes
        for node_id, info in self.model["nodes"].items():
            dim = len(info["attr"])
            lines.append(f"# {info['description']}")
            lines.append(f"{node_id.lower()} = Node('{node_id}', StateSpace.euclidean({dim}), [0.0]*{dim})")
            lines.append(f"hypergraph.add_node({node_id.lower()})")

        lines.append("")
        for h in self.model["handovers"]:
            lines.append(f"hypergraph.add_handover(Handover('{h['id']}', {h['src'].lower()}, {h['dst'].lower()}, Protocol.CONSERVATIVE))")

        return "\n".join(lines)

if __name__ == "__main__":
    print("🧪 [ARKHE] Iniciando Algoritmo de Destilação")

    # Exemplo: Ecossistema
    distiller = DistillationAlgorithm("Ecosystem-Sim")

    # Passos 1-6
    distiller.run_step(1, "Simular populações de coelhos e raposas.")
    distiller.run_step(2, [
        {"id": "Rabbit", "desc": "Presa"},
        {"id": "Fox", "desc": "Predador"},
        {"id": "Grass", "desc": "Recurso"}
    ])
    distiller.run_step(3, [
        {"id": "Eat", "src": "Rabbit", "dst": "Grass"},
        {"id": "Hunt", "src": "Fox", "dst": "Rabbit"}
    ])
    distiller.run_step(4, {
        "Rabbit": ["energy", "age"],
        "Fox": ["energy", "age"],
        "Grass": ["biomass"]
    })

    anl_code = distiller.export_anl()
    print("\n--- ANL Gerado via Destilação ---")
    print(anl_code)

    with open("ecosystem.arkhe", "w") as f:
        f.write(anl_code)
    print("\n✅ Arquivo ecosystem.arkhe gerado com sucesso.")
