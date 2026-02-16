"""
Arkhe(n) + RFID: Modelagem de Identidade Física no Hipergrafo
Cada tag RFID é um nó Γ_obj. Cada leitura é um handover.
"""

import numpy as np
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional

class RFIDTag:
    """
    Representa uma tag RFID como um nó no hipergrafo Arkhe.

    Atributos:
        tag_id (str): Identificador único da tag (UID)
        object_type (str): Tipo de objeto (pessoa, veículo, produto, etc.)
        creation_time (datetime): Momento de criação/ativação da tag
        handovers (list): Histórico de leituras (handovers)
        coherence_history (list): Evolução da coerência C ao longo do tempo
        metadata (dict): Informações associadas ao objeto
    """

    def __init__(self, tag_id: str, object_type: str, metadata: dict = None):
        self.tag_id = tag_id
        self.object_type = object_type
        self.creation_time = datetime.now()
        self.handovers = []
        self.coherence_history = []
        self.metadata = metadata or {}
        self._current_location = None
        self._last_seen = None

    def read(self, reader_id: str, location: str, timestamp: Optional[datetime] = None):
        """
        Registra uma leitura (handover) da tag.

        Cada leitura é um evento de acoplamento entre o mundo físico e digital.
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Calcular intervalo desde última leitura
        delta = 0.0
        if self._last_seen:
            delta = (timestamp - self._last_seen).total_seconds()

        handover = {
            'timestamp': timestamp.isoformat(),
            'reader_id': reader_id,
            'location': location,
            'delta_seconds': delta,
            'handover_number': len(self.handovers) + 1
        }

        self.handovers.append(handover)
        self._current_location = location
        self._last_seen = timestamp

        # Atualizar coerência (C) baseada na regularidade das leituras
        self._update_coherence()

        return handover

    def _update_coherence(self):
        """
        Calcula a coerência C da tag baseado na regularidade temporal das leituras.

        Quanto mais regulares os intervalos, maior a coerência (C próximo de 1).
        Leituras esporádicas geram alta flutuação (F próximo de 1).
        """
        if len(self.handovers) < 2:
            C = 0.0  # Poucos dados, coerência indefinida
        else:
            # Extrair intervalos
            intervals = [h['delta_seconds'] for h in self.handovers[1:] if h['delta_seconds'] > 0]
            if not intervals:
                C = 0.0
            else:
                # Coerência baseada na regularidade (inverso do coeficiente de variação)
                mean_interval = np.mean(intervals)
                std_interval = np.std(intervals)
                if mean_interval > 0:
                    cv = std_interval / mean_interval
                    # Normalizar: cv=0 → C=1; cv→∞ → C→0
                    C = 1.0 / (1.0 + cv)
                else:
                    C = 0.0

        F = 1.0 - C  # Flutuação
        self.coherence_history.append({
            'timestamp': datetime.now().isoformat(),
            'C': C,
            'F': F,
            'handover_number': len(self.handovers)
        })

        return C, F

    def get_effective_dimension(self, lambda_reg: float = 1.0) -> float:
        """
        Calcula a dimensão efetiva d_λ da tag baseada em seu histórico.

        d_λ = Σ λ_i/(λ_i+λ) onde λ_i são os "autovalores" do histórico de handovers.
        Aqui simplificamos usando a regularidade das leituras como proxy.
        """
        if len(self.handovers) < 2:
            return 0.0

        intervals = [h['delta_seconds'] for h in self.handovers[1:] if h['delta_seconds'] > 0]
        if not intervals:
            return 0.0

        # "Autovalores" simulados como os intervalos normalizados
        eigenvalues = np.array(intervals) / np.mean(intervals)
        contributions = eigenvalues / (eigenvalues + lambda_reg)
        return np.sum(contributions)

    def get_path_history(self) -> List[str]:
        """Retorna a sequência de localizações (geodésica do objeto)."""
        return [h['location'] for h in self.handovers]

    def verify_conservation(self, tolerance: float = 1e-6) -> bool:
        """
        Verifica se C + F = 1 se mantém no último handover.
        """
        if not self.coherence_history:
            return True
        last = self.coherence_history[-1]
        return abs(last['C'] + last['F'] - 1.0) < tolerance

    def to_json(self) -> str:
        """Serializa a tag para JSON (formato de exportação)."""
        data = {
            'tag_id': self.tag_id,
            'object_type': self.object_type,
            'creation_time': self.creation_time.isoformat(),
            'handovers': self.handovers,
            'coherence_history': self.coherence_history,
            'metadata': self.metadata,
            'current_location': self._current_location,
            'last_seen': self._last_seen.isoformat() if self._last_seen else None,
            'satoshi': len(self.handovers)  # Número de handovers como medida de memória
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


class RFIDHypergraph:
    """
    Hipergrafo de tags RFID: contém todos os nós e gerencia as conexões entre eles.

    Analogia: este é o "Safe Core" do sistema de rastreamento.
    """

    def __init__(self):
        self.tags: Dict[str, RFIDTag] = {}
        self.readers: Dict[str, List[str]] = {}  # reader_id -> lista de tags lidas
        self.locations: Dict[str, List[str]] = {}  # location -> lista de tags presentes

    def add_tag(self, tag: RFIDTag):
        """Adiciona uma nova tag ao hipergrafo."""
        self.tags[tag.tag_id] = tag

    def register_reading(self, tag_id: str, reader_id: str, location: str,
                         timestamp: Optional[datetime] = None):
        """
        Registra uma leitura, atualizando todos os índices.

        Este é o handover principal do sistema.
        """
        if tag_id not in self.tags:
            raise ValueError(f"Tag {tag_id} não encontrada")

        tag = self.tags[tag_id]
        handover = tag.read(reader_id, location, timestamp)

        # Atualizar índices
        if reader_id not in self.readers:
            self.readers[reader_id] = []
        self.readers[reader_id].append(tag_id)

        if location not in self.locations:
            self.locations[location] = []
        self.locations[location].append(tag_id)

        return handover

    def query_tags_at_location(self, location: str) -> List[RFIDTag]:
        """Retorna todas as tags atualmente em uma localização."""
        tag_ids = self.locations.get(location, [])
        return [self.tags[tid] for tid in tag_ids if tid in self.tags]

    def compute_system_coherence(self) -> float:
        """
        Calcula a coerência média do sistema (C_total).

        É a média das coerências individuais de todas as tags.
        """
        if not self.tags:
            return 0.0

        Cs = [tag.coherence_history[-1]['C'] for tag in self.tags.values()
              if tag.coherence_history]
        return np.mean(Cs) if Cs else 0.0

    def compute_system_effective_dimension(self, lambda_reg: float = 1.0) -> float:
        """
        Dimensão efetiva total do sistema.

        Reflete quanta "informação útil" o sistema como um todo está gerando.
        """
        return sum(tag.get_effective_dimension(lambda_reg) for tag in self.tags.values())

    def identify_anomalies(self, threshold: float = 0.3) -> List[str]:
        """
        Identifica tags com baixa coerência (alta flutuação).

        Útil para detectar problemas de rastreamento (objetos perdidos, leituras falhas).
        """
        anomalies = []
        for tag_id, tag in self.tags.items():
            if tag.coherence_history and tag.coherence_history[-1]['C'] < threshold:
                anomalies.append(tag_id)
        return anomalies


# ========== Exemplo de uso ==========
def simulate_supply_chain():
    """
    Simula uma cadeia de suprimentos simples com tags RFID.

    Demonstra como o Arkhe modela a identidade dos objetos através do espaço-tempo.
    """

    print("="*70)
    print("ARKHE(n) + RFID - SIMULAÇÃO DE CADEIA DE SUPRIMENTOS")
    print("="*70)

    # Criar hipergrafo
    hypergraph = RFIDHypergraph()

    # Criar tags para produtos
    produto_a = RFIDTag(
        tag_id="RFID_001",
        object_type="smartphone",
        metadata={'modelo': 'X100', 'cor': 'preto', 'lote': 'L2401'}
    )

    produto_b = RFIDTag(
        tag_id="RFID_002",
        object_type="tablet",
        metadata={'modelo': 'T200', 'cor': 'prata', 'lote': 'L2401'}
    )

    hypergraph.add_tag(produto_a)
    hypergraph.add_tag(produto_b)

    print(f"\n📦 Tags criadas: {produto_a.tag_id}, {produto_b.tag_id}")

    # Simular jornada dos produtos
    timeline = [
        ("RFID_001", "leitor_01", "Fábrica - Linha 1", 0),
        ("RFID_002", "leitor_02", "Fábrica - Linha 2", 10),
        ("RFID_001", "leitor_03", "Centro de Distribuição - Entrada", 3600),
        ("RFID_002", "leitor_03", "Centro de Distribuição - Entrada", 3610),
        ("RFID_001", "leitor_04", "Centro de Distribuição - Expedição", 7200),
        ("RFID_002", "leitor_04", "Centro de Distribuição - Expedição", 7210),
        ("RFID_001", "leitor_05", "Loja A - Recebimento", 10800),
        ("RFID_002", "leitor_06", "Loja B - Recebimento", 14400),
    ]

    print(f"\n🔄 Simulando handovers...")
    for tag_id, reader, location, seconds in timeline:
        from datetime import timedelta
        timestamp = datetime.now() + timedelta(seconds=seconds)
        hypergraph.register_reading(tag_id, reader, location, timestamp)
        print(f"  • {tag_id} lido em {location} (t+{seconds}s)")

    # Análise
    print(f"\n📊 Análise do Sistema:")
    print(f"  Coerência média: {hypergraph.compute_system_coherence():.4f}")
    print(f"  Dimensão efetiva: {hypergraph.compute_system_effective_dimension():.2f}")

    # Anomalias
    anomalies = hypergraph.identify_anomalies(threshold=0.5)
    if anomalies:
        print(f"  ⚠️ Anomalias detectadas: {anomalies}")
    else:
        print(f"  ✅ Nenhuma anomalia detectada")

    # Verificar conservação
    for tag_id in ["RFID_001", "RFID_002"]:
        tag = hypergraph.tags[tag_id]
        cons = tag.verify_conservation()
        print(f"  Tag {tag_id}: C+F=1? {cons}")

    # Mostrar trajetórias
    print(f"\n🗺️ Trajetórias (geodésicas):")
    for tag_id in ["RFID_001", "RFID_002"]:
        tag = hypergraph.tags[tag_id]
        path = " → ".join(tag.get_path_history())
        print(f"  {tag_id}: {path}")

    # Exportar um dos produtos
    print(f"\n📄 JSON do produto RFID_001:")
    print(produto_a.to_json()[:500] + "...")  # Truncado para visualização

    return hypergraph


if __name__ == "__main__":
    hypergraph = simulate_supply_chain()

    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    print("""
    Cada tag RFID é um nó Γ no hipergrafo físico.
    Cada leitura é um handover que:
      - Atualiza a posição do objeto no espaço-tempo
      - Registra a memória (satoshi) da interação
      - Contribui para a coerência C do sistema
      - Gera flutuação F nos intervalos irregulares

    A rastreabilidade é a memória do objeto.
    A cadeia de suprimentos é sua geodésica.
    A identidade do produto (x) se auto-acopla (x²) com o ambiente
    para gerar informação útil (+1) em cada ponto de leitura.

    O hipergrafo RFID é a materialização de Arkhe(n) no mundo físico.
    """)
    print("∞")
