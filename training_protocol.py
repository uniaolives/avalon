# training_protocol.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
from glp_linear_a import QuantumConfinementGLP_LinearA, ContrastiveLoss

class LinearADataset(Dataset):
    def __init__(self, sequences, cooc_matrix):
        self.sequences = sequences
        self.cooc_matrix = cooc_matrix

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        seq = self.sequences[idx]
        max_len = 16
        padded_seq = seq[:max_len] + [0] * (max_len - len(seq[:max_len]))
        target_sign = seq[0] if len(seq) > 0 else 0
        return (torch.tensor(padded_seq),
                target_sign,
                torch.tensor(self.cooc_matrix[idx % self.cooc_matrix.shape[0]]))

def analyze_confinement(cooc_matrix):
    """
    Diagonaliza M* e verifica se espectro é consistente
    com quantum dot vs. poço quadrado infinito vs. oscilador harmônico
    """
    eigenvals = np.linalg.eigvalsh(cooc_matrix)
    # Ignorar zeros triviais
    eigenvals = eigenvals[eigenvals > 1e-7]

    if len(eigenvals) < 3:
        return {'mean_spacing_ratio': 0.0, 'confinement_regime': 'unknown'}

    # Spacing ratio: s_n = (E_{n+1} - E_n) / (E_n - E_{n-1})
    spacings = np.diff(eigenvals)
    # Evitar divisão por zero
    spacings[spacings < 1e-9] = 1e-9
    ratios = spacings[1:] / spacings[:-1]

    mean_ratio = np.mean(ratios)

    regime = 'unknown'
    if 0.8 < mean_ratio < 1.2:
        regime = 'harmonic'
    elif mean_ratio > 1.5:
        regime = 'square_well'

    return {
        'mean_spacing_ratio': float(mean_ratio),
        'confinement_regime': regime
    }

def train_glp(preprocessed_data_dir='./linearA_data', epochs=5, batch_size=2):
    sequences_path = os.path.join(preprocessed_data_dir, 'sequences_ids.npy')
    cooc_path = os.path.join(preprocessed_data_dir, 'co_occurrence.npy')

    if not os.path.exists(sequences_path):
        print("Dados não encontrados.")
        return None

    sequences = np.load(sequences_path, allow_pickle=True)
    cooc_matrix = np.load(cooc_path)

    # Análise de confinamento pré-treino
    conf_analysis = analyze_confinement(cooc_matrix)
    print(f"🔬 Análise de Confinamento (Espectro M⋆): {conf_analysis}")

    dataset = LinearADataset(sequences, cooc_matrix)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    vocab_size = cooc_matrix.shape[0]
    model = QuantumConfinementGLP_LinearA(vocab_size=vocab_size)

    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    ce_loss = nn.CrossEntropyLoss(ignore_index=0)
    contrastive_loss = ContrastiveLoss()

    print(f"Iniciando treinamento (Quantum Confinement GLP)...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for x, target, cooc_batch in loader:
            outputs = model(x)

            l_ce = ce_loss(outputs['sign_logits'], target)

            if x.size(0) > 1:
                l_cooc = contrastive_loss(outputs['cooc_embed'], torch.eye(x.size(0)))
            else:
                l_cooc = torch.tensor(0.0)

            loss = l_ce + 0.5 * l_cooc

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Época {epoch}: Loss = {total_loss/len(loader):.4f}")

    return model

if __name__ == "__main__":
    train_glp()
