# glp_linear_a.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class ConfinementLayer(nn.Module):
    """
    Camada de confinamento para uma escala específica.
    Implementa um "quantum dot" de informação.
    """
    def __init__(self, window_size, embed_dim=64, hidden_dim=128, potential='exponential'):
        super().__init__()
        self.window_size = window_size
        # Convolução atua como o Hamiltoniano local no poço
        self.conv = nn.Conv1d(embed_dim, hidden_dim, kernel_size=window_size, padding=window_size//2)
        self.potential_type = potential

    def forward(self, x):
        # x: [batch, seq_len, embed_dim]
        x = x.transpose(1, 2) # [batch, embed_dim, seq_len]
        out = self.conv(x)

        # Aplica "potencial" de confinamento (opcional, aqui simplificado com ativação)
        if self.potential_type == 'gaussian':
            out = out * torch.exp(-torch.arange(out.size(-1)).to(out.device)**2 / (2 * self.window_size**2))

        return F.gelu(out)

class CrossScaleAttention(nn.Module):
    """
    Mecanismo de tunelamento entre diferentes poços de confinamento.
    """
    def __init__(self, num_scales, hidden_dim):
        super().__init__()
        self.attn = nn.MultiheadAttention(hidden_dim, num_heads=4, batch_first=True)

    def forward(self, scale_reprs):
        # scale_reprs: [batch, num_scales, hidden_dim]
        attn_out, _ = self.attn(scale_reprs, scale_reprs, scale_reprs)
        return attn_out

class QuantumConfinementGLP_LinearA(nn.Module):
    """
    Modelo de Confinamento Quântico para Linear A.
    Superlattice de poços (escalas) com tunelamento (atenção).
    """
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, scales=[2, 3, 5, 7, 15]):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.pos_embed = nn.Parameter(torch.randn(1, 256, embed_dim))

        self.quantum_dots = nn.ModuleList([
            ConfinementLayer(window_size=s, embed_dim=embed_dim, hidden_dim=hidden_dim)
            for s in scales
        ])

        self.tunneling = CrossScaleAttention(num_scales=len(scales), hidden_dim=hidden_dim)

        self.classifier = nn.Linear(hidden_dim, vocab_size)
        self.cooc_proj = nn.Linear(hidden_dim, embed_dim)

    def forward(self, x):
        # x: [batch, seq_len]
        batch, seq_len = x.shape
        e = self.embedding(x) + self.pos_embed[:, :seq_len, :]

        # Cada escala produz seus "estados ligados"
        scale_outputs = []
        for dot in self.quantum_dots:
            out = dot(e) # [batch, hidden_dim, seq_len]
            # Pooling para obter representação da escala
            scale_outputs.append(out.mean(dim=-1))

        # Tunelamento entre escalas
        scale_reprs = torch.stack(scale_outputs, dim=1) # [batch, n_scales, hidden_dim]
        tunneled_reprs = self.tunneling(scale_reprs)

        # Representação final (média das escalas tuneladas)
        final_repr = tunneled_reprs.mean(dim=1)

        return {
            'tablet_repr': final_repr,
            'sign_logits': self.classifier(final_repr),
            'cooc_embed': self.cooc_proj(final_repr)
        }

class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=0.07):
        super().__init__()
        self.temperature = temperature

    def forward(self, embeddings, cooccurrence_matrix):
        norm_emb = F.normalize(embeddings, dim=1)
        sim_matrix = torch.matmul(norm_emb, norm_emb.T) / self.temperature
        exp_sim = torch.exp(sim_matrix)

        # Para simplificar, assumimos que a diagonal de cooc_matrix
        # ou valores altos representam vizinhos positivos
        pos_mask = (cooccurrence_matrix > 0.1).float()
        pos_sim = (exp_sim * pos_mask).sum(dim=1)
        all_sim = exp_sim.sum(dim=1)

        return -torch.log(pos_sim / (all_sim + 1e-8) + 1e-8).mean()
