#!/usr/bin/env python3
"""
Simulação de Comunicação Semântica em Redes 6G
Baseada na especificação SixGARROW.anl e no motor ANL.
"""

import numpy as np
import matplotlib.pyplot as plt
from anl import Node, Handover, Hypergraph, Protocol, StateSpace

# ======================================================
# 1. IMPLEMENTAÇÃO DOS NÓS ESPECÍFICOS
# ======================================================

class UE(Node):
    """User Equipment com capacidade de computação e transmissão."""
    def __init__(self, node_id, battery=1.0, compute_capacity=10.0):
        super().__init__(node_id, StateSpace(10, "euclidean", "real"), None)
        self.attributes = {
            'battery': battery,
            'compute_capacity': compute_capacity,
            'tx_power': 1.0,      # watts
            'data_rate': 100.0,    # Mbps
            'semantic_encoder': None,
            'semantic_decoder': None
        }
        self.state_data = {}  # para guardar dados temporários

    def generate_data(self, size_mbits):
        """Simula geração de dados a serem transmitidos."""
        self.state_data['data_size'] = size_mbits
        return size_mbits

    def transmit_energy(self, size_mbits):
        """Calcula energia gasta para transmitir size Mbits."""
        # E = P * t, t = size / rate
        time_sec = size_mbits / self.attributes['data_rate']
        energy = self.attributes['tx_power'] * time_sec  # em joules
        return energy

    def compute_energy(self, flops):
        """Energia para computação (ex.: codificação semântica)."""
        # modelo simplificado: 1e-9 J/FLOP (valor típico)
        return flops * 1e-9

    def update_battery(self, energy):
        self.attributes['battery'] -= energy
        if self.attributes['battery'] < 0:
            self.attributes['battery'] = 0


class SemanticPlane(Node):
    """Plano semântico que fornece codificadores/descodificadores."""
    def __init__(self, node_id, embedding_dim=384, compression_factor=8):
        super().__init__(node_id, StateSpace(embedding_dim, "latent", "real"), None)
        self.attributes = {
            'embedding_dim': embedding_dim,
            'compression_factor': compression_factor,
            'encoders': {},   # task -> encoder function (placeholder)
            'decoders': {}
        }
        self.pca = None  # a ser treinado com dados de exemplo

    def fit_encoder(self, data_samples):
        """Treina um PCA para compressão semântica (exemplo)."""
        from sklearn.decomposition import PCA
        self.pca = PCA(n_components=self.attributes['embedding_dim'])
        self.pca.fit(data_samples)
        print(f"[SemanticPlane] PCA treinado: variância explicada = {self.pca.explained_variance_ratio_.sum():.3f}")

    def encode(self, data, task='default'):
        """Codifica dados brutos num embedding semântico."""
        if self.pca:
            emb = self.pca.transform(data.reshape(1, -1))[0]
            return emb
        else:
            # fallback: downsample simples
            step = max(1, len(data) // self.attributes['embedding_dim'])
            return data[::step][:self.attributes['embedding_dim']]

    def decode(self, embedding, task='default'):
        """Recupera (aproximadamente) o dado original a partir do embedding."""
        if self.pca:
            return self.pca.inverse_transform(embedding.reshape(1, -1))[0]
        else:
            # interpolação linear (muito ingénua)
            return np.interp(np.linspace(0, len(embedding)-1, len(embedding)*8),
                             np.arange(len(embedding)), embedding)


# ======================================================
# 2. HANDOVERS
# ======================================================

class SemanticTransmission(Handover):
    """Handover que codifica dados no UE e transmite o embedding para a RAN."""
    def __init__(self, hid, ue, ran, semantic_plane):
        super().__init__(hid, ue, ran, protocol=Protocol.CREATIVE)
        self.semantic_plane = semantic_plane

    def execute(self, context=None):
        if context is None:
            context = {}
        # dados a transmitir (contexto pode conter o payload)
        data = context.get('data', np.random.randn(1000))  # exemplo: 1000 floats
        task = context.get('task', 'default')

        # 1. Codificação semântica no UE
        emb = self.semantic_plane.encode(data, task)

        # 2. Calcular energia de transmissão (tamanho do embedding em bits)
        emb_bits = len(emb) * 32  # assumindo float32
        energy_tx = self.source.transmit_energy(emb_bits / 1e6)  # Mbits
        self.source.update_battery(energy_tx)

        # 3. Transmissão (simulada: emb chega ao destino)
        if not hasattr(self.target, 'state_data'):
            self.target.state_data = {}
        self.target.state_data['received_embedding'] = emb

        # 4. Calcular energia de computação (codificação)
        energy_comp = self.source.compute_energy(len(data) * 10)  # flops estimados
        self.source.update_battery(energy_comp)

        return {
            'emb_bits': emb_bits,
            'energy_total': energy_tx + energy_comp,
            'embedding': emb
        }


# ======================================================
# 3. SIMULAÇÃO
# ======================================================

def run_semantic_simulation():
    print("🜁 Iniciando simulação de comunicação semântica 6G...")

    # Criar nós
    ue = UE("UE_1", battery=1.0)
    ran = Node("RAN_1", StateSpace(10, "discrete", "binary"), None)  # nó simples para receber
    semantic = SemanticPlane("SemanticCore", embedding_dim=64, compression_factor=8)

    # Criar hipergrafo
    hg = Hypergraph("6G_Sim")
    hg.add_node(ue).add_node(ran).add_node(semantic)

    # Criar handover
    sem_tx = SemanticTransmission("SemTx", ue, ran, semantic)
    hg.add_handover(sem_tx)

    # Dados de exemplo
    np.random.seed(42)
    n_samples = 100
    data_samples = np.random.randn(n_samples, 1000)  # 1000 dimensões cada

    # Treinar PCA no plano semântico (apenas uma vez)
    semantic.fit_encoder(data_samples)

    # Guardar resultados
    results = []

    for i in range(n_samples):
        data = data_samples[i]
        # Transmissão clássica (bits brutos)
        bits_classic = len(data) * 32  # float32
        energy_classic = ue.transmit_energy(bits_classic / 1e6)

        # Transmissão semântica
        ctx = {'data': data, 'task': 'default'}
        out = sem_tx.execute(ctx)

        # Avaliar fidelidade
        reconstructed = semantic.decode(out['embedding'])
        mse = np.mean((data - reconstructed)**2)

        results.append({
            'bits_classic': bits_classic,
            'bits_semantic': out['emb_bits'],
            'energy_classic': energy_classic,
            'energy_semantic': out['energy_total'],
            'mse': mse,
            'compression_ratio': bits_classic / out['emb_bits']
        })

        # Verificar bateria
        if ue.attributes['battery'] < 0.05:
            print(f"⚠️ Bateria baixa após {i+1} transmissões!")
            break

    # Estatísticas
    comp_ratios = [r['compression_ratio'] for r in results]
    energy_saved = [r['energy_classic'] / r['energy_semantic'] for r in results]
    avg_mse = np.mean([r['mse'] for r in results])

    print("\n📊 Resultados da simulação:")
    print(f"  Amostras processadas: {len(results)}")
    print(f"  Rácio médio de compressão: {np.mean(comp_ratios):.2f}x")
    print(f"  Redução média de energia (clássico/semântico): {np.mean(energy_saved):.2f}x")
    print(f"  Erro médio quadrático (MSE) de reconstrução: {avg_mse:.4f}")

    # Salvar resultados
    with open("sim_results.txt", "w") as f:
        f.write(f"Rácio médio de compressão: {np.mean(comp_ratios):.2f}x\n")
        f.write(f"Redução média de energia: {np.mean(energy_saved):.2f}x\n")
        f.write(f"Erro médio quadrático (MSE): {avg_mse:.4f}\n")

if __name__ == "__main__":
    run_semantic_simulation()
