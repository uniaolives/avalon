# training_protocol.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F
import numpy as np
import os
from glp_second_quantization import BCD_GLPLinearA, QuantumActionLoss

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
        return (torch.tensor(padded_seq),
                torch.tensor(padded_seq)) # Targets are the signs themselves for CE

def analyze_confinement(cooc_matrix):
    eigenvals = np.linalg.eigvalsh(cooc_matrix)
    eigenvals = eigenvals[eigenvals > 1e-7]
    if len(eigenvals) < 3:
        return {'mean_spacing_ratio': 0.0, 'confinement_regime': 'unknown'}
    spacings = np.diff(eigenvals)
    spacings[spacings < 1e-9] = 1e-9
    ratios = spacings[1:] / spacings[:-1]
    mean_ratio = np.mean(ratios)
    regime = 'unknown'
    if 0.8 < mean_ratio < 1.2:
        regime = 'harmonic'
    elif mean_ratio > 1.5:
        regime = 'square_well'
    return {'mean_spacing_ratio': float(mean_ratio), 'confinement_regime': regime}

def measure_quantum_coherence(model, test_loader):
    """
    Mede 'coerência quântica' do modelo.
    """
    model.eval()
    fidelities = []
    with torch.no_grad():
        for x, _ in test_loader:
            # Original state
            out1 = model(x, return_wavefunction=True)

            # Perturbed state: mask some signs
            masked = x.clone()
            mask = torch.rand_like(masked.float()) > 0.3
            masked[mask] = 0
            out2 = model(masked, return_wavefunction=True)

            # Fidelity: |⟨ψ₁|ψ₂⟩|²
            wf1 = F.normalize(out1['tunneled_states'].flatten(1), dim=1)
            wf2 = F.normalize(out2['tunneled_states'].flatten(1), dim=1)
            fidelity = (wf1 * wf2).sum(dim=1)**2
            fidelities.append(fidelity.mean().item())

    return np.mean(fidelities)

def train_glp(preprocessed_data_dir='./linearA_data', epochs=5, batch_size=2):
    sequences_path = os.path.join(preprocessed_data_dir, 'sequences_ids.npy')
    cooc_path = os.path.join(preprocessed_data_dir, 'co_occurrence.npy')

    if not os.path.exists(sequences_path):
        print("Dados não encontrados.")
        return None

    sequences = np.load(sequences_path, allow_pickle=True)
    cooc_matrix = np.load(cooc_path)

    # Análise de confinamento
    conf_analysis = analyze_confinement(cooc_matrix)
    print(f"🔬 Análise de Confinamento: {conf_analysis}")

    dataset = LinearADataset(sequences, cooc_matrix)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    vocab_size = cooc_matrix.shape[0]
    model = BCD_GLPLinearA(vocab_size=vocab_size)

    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    action_loss_fn = QuantumActionLoss()

    print(f"Iniciando treinamento (B*C*D GLP)...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for x, targets in loader:
            # Forward with wavefunction return for kinetic loss
            outputs = model(x, return_wavefunction=True)

            loss, loss_details = action_loss_fn(outputs, targets, outputs)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Época {epoch}: Loss = {total_loss/len(loader):.4f} (Pot: {loss_details['potential']:.3f}, Kin: {loss_details['kinetic']:.3f}, Tun: {loss_details['tunnel']:.3f})")

    coherence = measure_quantum_coherence(model, loader)
    print(f"✨ Coerência Quântica Final: {coherence:.4f}")

    return model

if __name__ == "__main__":
    train_glp()
