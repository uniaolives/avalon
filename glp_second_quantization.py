# glp_second_quantization.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math
from scipy.special import hermite

class HarmonicConfinement(nn.Module):
    """
    Poço harmônico quântico para sequências.
    Estados: |n⟩ com energia E_n = ℏω(n + 1/2)
    No espaço de embedding: polinômios de Hermite × envelope gaussiano
    """
    def __init__(self, max_n=8, sigma=1.0):
        super().__init__()
        self.max_n = max_n  # número de níveis quânticos
        self.sigma = sigma  # largura do poço harmônico

        # Autofunções do oscilador harmônico (pré-computadas)
        self.register_buffer(
            'hermite_basis',
            self._compute_hermite_basis(max_n, 256)  # discretização da posição
        )

    def _compute_hermite_basis(self, max_n, resolution):
        x = torch.linspace(-3, 3, resolution)
        xi = x / (self.sigma * np.sqrt(2))

        basis = []
        for n in range(max_n):
            # Using scipy.special.hermite to get polynomial coefficients
            H_n_poly = hermite(n)
            H_n_vals = torch.tensor(H_n_poly(xi.numpy()), dtype=torch.float32)
            norm = (2**n * math.factorial(n) * np.sqrt(np.pi))**(-0.5)
            psi = norm * H_n_vals * torch.exp(-xi**2 / 2)
            basis.append(psi)

        return torch.stack(basis)  # [max_n, resolution]

    def forward(self, positions, amplitudes):
        """
        positions: índices normalizados na sequência [-1, 1], shape [batch, seq_len]
        amplitudes: ocupação de cada modo |n⟩, shape [batch, max_n]
        """
        batch, seq_len = positions.shape
        # Interpolação das autofunções nas posições reais
        idx = ((positions + 1) / 2 * 255).long().clamp(0, 255) # [batch, seq_len]

        # self.hermite_basis: [max_n, 256]
        # We need to sample from basis for each position in the batch
        # basis_sampled: [batch, max_n, seq_len]
        basis_sampled = self.hermite_basis[:, idx] # This indexing might need to be careful
        # Correct indexing for [max_n, batch, seq_len]
        basis_sampled = self.hermite_basis.index_select(1, idx.view(-1)).view(self.max_n, batch, seq_len)
        basis_sampled = basis_sampled.permute(1, 0, 2) # [batch, max_n, seq_len]

        # Composição coerente dos estados
        # wavefunction = torch.einsum('bn,bnl->bl', amplitudes, basis_sampled)
        wavefunction = (amplitudes.unsqueeze(-1) * basis_sampled).sum(dim=1)
        return wavefunction


class SuperlatticeHamiltonian(nn.Module):
    """
    Múltiplos poços harmônicos acoplados.
    Cada escala = modo coletivo do cristal.
    """
    def __init__(self, hidden_dim, scales=[2, 3, 5, 8, 13, 21], coupling_matrix=None):
        """
        Escalas: números de Fibonacci (proporção áurea entre poços)
        """
        super().__init__()
        self.scales = scales
        self.n_wells = len(scales)
        self.hidden_dim = hidden_dim

        # Hamiltoniano de cada poço isolado
        self.wells = nn.ModuleList([
            HarmonicConfinement(max_n=min(s, 8), sigma=s/5)
            for s in scales
        ])

        # Matriz de acoplamento (tunelamento entre poços)
        if coupling_matrix is None:
            coupling = torch.exp(-torch.abs(
                torch.tensor(scales, dtype=torch.float32).unsqueeze(0) -
                torch.tensor(scales, dtype=torch.float32).unsqueeze(1)
            ) / 2.0)
            coupling = coupling - torch.diag(torch.diag(coupling))
        else:
            coupling = coupling_matrix

        self.register_buffer('coupling', coupling)

        self.omega = nn.Parameter(
            torch.tensor([1.0/s for s in scales])
        )

        # Layers to learn occupation amplitudes from embedding
        self.occupation_heads = nn.ModuleList([
            nn.Linear(hidden_dim, well.max_n)
            for well in self.wells
        ])

    def forward(self, sequence_embedding):
        """
        sequence_embedding: [batch, seq_len, dim]
        """
        batch, seq_len, dim = sequence_embedding.shape

        # Posições normalizadas no poço harmônico
        positions = torch.linspace(-1, 1, seq_len).to(sequence_embedding.device).unsqueeze(0).expand(batch, -1)

        # Mean embedding for the sequence to determine well occupation
        # In a more advanced version, this could be per-token
        seq_mean = sequence_embedding.mean(dim=1) # [batch, dim]

        well_states = []
        for i, well in enumerate(self.wells):
            amps = self.occupation_heads[i](seq_mean).softmax(dim=-1) # [batch, max_n]
            wavefunction = well(positions, amps) # [batch, seq_len]
            # Broadcast wavefunction to hidden_dim
            # (Simulating that the wavefunction modulates the hidden state)
            well_states.append(wavefunction.unsqueeze(-1) * seq_mean.unsqueeze(1))

        return torch.stack(well_states, dim=1)  # [batch, n_wells, seq_len, hidden_dim]


class ResonantTunnelingAttention(nn.Module):
    """
    Tunelamento ressonante como mecanismo de atenção.
    """
    def __init__(self, n_wells, hidden_dim, temperature=0.1):
        super().__init__()
        self.n_wells = n_wells
        self.hidden_dim = hidden_dim
        self.temperature = temperature

        self.S_matrix = nn.Parameter(
            torch.randn(n_wells, n_wells, hidden_dim) * 0.1
        )

        self.resonance_energy = nn.Parameter(torch.randn(n_wells, hidden_dim))
        self.resonance_width = nn.Parameter(torch.ones(n_wells, hidden_dim) * 0.1)

    def breit_wigner(self, E, E_0, Γ):
        """Amplitude de transmissão perto de ressonância (complexo aproximado por abs)."""
        # Complex: Γ / ((E - E_0) + 1j * Γ/2)
        # Abs: Γ / sqrt((E - E_0)^2 + (Γ/2)^2)
        denom = torch.sqrt((E - E_0)**2 + (Γ/2)**2 + 1e-8)
        return Γ / denom

    def forward(self, well_states, query_energy=None):
        """
        well_states: [batch, n_wells, seq_len, hidden_dim]
        """
        batch, n_wells, seq_len, hidden = well_states.shape

        if query_energy is None:
            query_energy = well_states.mean(dim=[1, 2])  # [batch, hidden]

        E = query_energy.unsqueeze(1)  # [batch, 1, hidden]
        E_0 = self.resonance_energy.unsqueeze(0)  # [1, n_wells, hidden]
        Γ = torch.abs(self.resonance_width).unsqueeze(0)

        tunneling_amp = self.breit_wigner(E, E_0, Γ)  # [batch, n_wells, hidden]

        S = F.softmax(self.S_matrix / self.temperature, dim=1)
        S = S.unsqueeze(0).expand(batch, -1, -1, -1)  # [batch, n_wells, n_wells, hidden]

        mixed_states = torch.einsum('bijh,bjsh->bish', S, well_states)
        output = mixed_states * tunneling_amp.unsqueeze(2)

        return output, tunneling_amp


class BCD_GLPLinearA(nn.Module):
    """
    GLP completo: B*C*D = Harmônico × Superlattice × Tunelamento
    """
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        self.hamiltonian = SuperlatticeHamiltonian(
            hidden_dim=embed_dim,
            scales=[2, 3, 5, 8, 13, 21]
        )

        self.tunneling = ResonantTunnelingAttention(
            n_wells=6,
            hidden_dim=embed_dim
        )

        self.sign_predictor = nn.Linear(embed_dim, vocab_size)
        self.geometry_probe = nn.Linear(embed_dim, 3)
        self.vacuum = nn.Parameter(torch.randn(embed_dim))

    def forward(self, sign_ids, return_wavefunction=False):
        x = self.embedding(sign_ids)
        well_states = self.hamiltonian(x)
        tunneled, probs = self.tunneling(well_states)

        # Colapso: superposição coerente
        final_state = tunneled.sum(dim=1) # [batch, seq_len, embed_dim]

        output = {
            'tablet_repr': final_state.mean(dim=1),
            'sign_logits': self.sign_predictor(final_state),
            'geometry': self.geometry_probe(final_state.mean(dim=1)),
            'scale_probabilities': probs,
            'tunneling_strength': probs.std(dim=1).mean()
        }

        if return_wavefunction:
            output['well_states'] = well_states
            output['tunneled_states'] = tunneled

        return output


class QuantumActionLoss(nn.Module):
    def __init__(self, alpha_kinetic=1.0, alpha_potential=1.0, alpha_tunnel=0.5):
        super().__init__()
        self.alpha_kinetic = alpha_kinetic
        self.alpha_potential = alpha_potential
        self.alpha_tunnel = alpha_tunnel

    def forward(self, predictions, targets, model_states):
        # potential loss: cross entropy
        potential = F.cross_entropy(
            predictions['sign_logits'].view(-1, predictions['sign_logits'].size(-1)),
            targets.view(-1)
        )

        # kinetic loss: smoothness
        states = model_states['tunneled_states'] # [batch, n_wells, seq_len, hidden]
        kinetic = ((states[:, :, 1:, :] - states[:, :, :-1, :])**2).mean()

        # tunnel loss
        tunnel_energy = -torch.log(predictions['tunneling_strength'] + 1e-8)

        total = (self.alpha_potential * potential +
                self.alpha_kinetic * kinetic +
                self.alpha_tunnel * tunnel_energy)

        return total, {
            'potential': potential.item(),
            'kinetic': kinetic.item(),
            'tunnel': tunnel_energy.item()
        }
