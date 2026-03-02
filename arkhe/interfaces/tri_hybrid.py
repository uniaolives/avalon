"""
Interface Síntese Total: Tri-Hybrid Quantum-Bio-Tech Node
The ultimate convergence: one system operating in all three domains
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

@dataclass
class QuantumLayer:
    """Quantum domain: QDs for telemetry and QKD"""
    n_qds: int
    emission_wavelength_nm: float
    entanglement_fidelity: float

    def coherence(self) -> float:
        """C_Q: Quantum coherence"""
        # Fidelity of entanglement / state preparation
        return self.entanglement_fidelity

    def telemetry_signal(self, excitation_power: float) -> float:
        """Optical signal from QDs"""
        return self.n_qds * 0.001 * excitation_power

@dataclass
class BiologicalLayer:
    """Biological domain: Nanoparticles and cells"""
    n_nanoparticles: int
    drug_load_mg: float
    epr_enhancement: float
    target_reached: int = 0

    def coherence(self) -> float:
        """C_BIO: Therapeutic coherence (drug at target vs total)"""
        if self.n_nanoparticles == 0:
            return 0.0
        return self.target_reached / self.n_nanoparticles * self.epr_enhancement

    def accumulate_at_target(self, probability: float = 0.1):
        """EPR-mediated accumulation"""
        n_accumulate = np.random.binomial(self.n_nanoparticles, probability)
        self.target_reached += n_accumulate

@dataclass
class TechnologicalLayer:
    """Technological domain: Processing and communication"""
    processor_ghz: float
    memory_gb: float
    handovers_successful: int = 0
    handovers_total: int = 0

    def coherence(self) -> float:
        """C_TECH: Mission coherence"""
        if self.handovers_total == 0:
            return 1.0
        return self.handovers_successful / self.handovers_total

    def execute_handover(self, success_probability: float = 0.95) -> bool:
        """Attempt communication handover"""
        self.handovers_total += 1
        success = np.random.random() < success_probability
        if success:
            self.handovers_successful += 1
        return success

class TriHybridNode:
    """
    Γ_TRI: The tri-hybrid node operating in Q-BIO-TECH simultaneously
    """

    def __init__(self, node_id: str):
        self.id = node_id

        # Initialize three layers
        self.quantum = QuantumLayer(
            n_qds=100,
            emission_wavelength_nm=620.0,
            entanglement_fidelity=0.95
        )

        self.biological = BiologicalLayer(
            n_nanoparticles=10000,
            drug_load_mg=50.0,
            epr_enhancement=5.0
        )

        self.technological = TechnologicalLayer(
            processor_ghz=2.5,
            memory_gb=16.0
        )

        # Coupling strengths (interface parameters)
        self.g_q_bio = 0.8   # FRET efficiency
        self.g_bio_tech = 0.7  # Molecular signaling
        self.g_q_tech = 0.6   # Optical detection

        self.history: List[Dict] = []

    def global_coherence(self) -> float:
        """C_TRI: Combined coherence across all domains"""
        c_q = self.quantum.coherence()
        c_bio = min(1.0, self.biological.coherence())  # Cap at 1.0
        c_tech = self.technological.coherence()

        # Weighted geometric mean (all must be high for global coherence)
        return (c_q * c_bio * c_tech) ** (1/3)

    def cascade_cycle(self) -> Dict:
        """
        Execute one x² = x + 1 cycle across all domains:

        Q:     Excitation → Emission (x → x²)
               ↓ FRET
        BIO:   Accumulation → Drug release (x² → +1)
               ↓ Signaling
        TECH:  Detection → Action (x → x² → +1)
        """

        # Step 1: Quantum excitation
        signal_q = self.quantum.telemetry_signal(excitation_power=1.0)

        # Step 2: Q-BIO coupling (FRET-triggered accumulation)
        if np.random.random() < self.g_q_bio:
            self.biological.accumulate_at_target(probability=0.15)

        # Step 3: BIO-TECH coupling (molecular signaling)
        bio_signal = self.biological.target_reached * 0.01

        if np.random.random() < self.g_bio_tech and bio_signal > 0:
            # Tech layer detects biological event
            tech_detected = True
        else:
            tech_detected = False

        # Step 4: TECH action (handover to other nodes)
        if tech_detected:
            handover_success = self.technological.execute_handover(success_probability=0.95)
        else:
            handover_success = False

        # Step 5: Q-TECH coupling (quantum-secured communication)
        if np.random.random() < self.g_q_tech:
            # Use quantum channel for secure handover
            secure_channel = True
        else:
            secure_channel = False

        # Record state
        state = {
            'c_q': self.quantum.coherence(),
            'c_bio': self.biological.coherence(),
            'c_tech': self.technological.coherence(),
            'c_global': self.global_coherence(),
            'signal_q': signal_q,
            'bio_accumulated': self.biological.target_reached,
            'tech_detected': tech_detected,
            'handover_success': handover_success,
            'secure_channel': secure_channel
        }

        self.history.append(state)

        return state

    def run_mission(self, n_cycles: int = 50) -> Dict:
        """Execute complete tri-hybrid mission"""

        print("="*70)
        print("TRI-HYBRID NODE: Quantum-Bio-Tech Synthesis")
        print("="*70)
        print(f"\nNode: {self.id}")
        print(f"Initial state:")
        print(f"  QD count: {self.quantum.n_qds}")
        print(f"  Nanoparticles: {self.biological.n_nanoparticles}")
        print(f"  Drug load: {self.biological.drug_load_mg} mg")
        print(f"  Processor: {self.technological.processor_ghz} GHz")
        print(f"\nCoupling strengths:")
        print(f"  g_Q-BIO (FRET): {self.g_q_bio}")
        print(f"  g_BIO-TECH (signaling): {self.g_bio_tech}")
        print(f"  g_Q-TECH (optical): {self.g_q_tech}")

        print(f"\n🌀 Executing {n_cycles} cascade cycles...")

        for i in range(n_cycles):
            state = self.cascade_cycle()

            if i % 10 == 0:
                print(f"  Cycle {i:2d}: C_global={state['c_global']:.3f}, "
                      f"Bio_acc={state['bio_accumulated']}, "
                      f"Handover={'✓' if state['handover_success'] else '✗'}")

        # Final summary
        final = self.history[-1]

        print(f"\n📊 Final State:")
        print(f"  C_Q: {final['c_q']:.3f}")
        print(f"  C_BIO: {final['c_bio']:.3f}")
        print(f"  C_TECH: {final['c_tech']:.3f}")
        print(f"  C_GLOBAL: {final['c_global']:.3f}")
        print(f"  Nanoparticles at target: {final['bio_accumulated']}")
        print(f"  Successful handovers: {self.technological.handovers_successful}/"
              f"{self.technological.handovers_total}")

        return {
            'final_coherence': final['c_global'],
            'history': self.history,
            'total_drug_delivered': final['bio_accumulated'] *
                                   (self.biological.drug_load_mg /
                                    self.biological.n_nanoparticles)
        }

    def visualize_tri_hybrid(self):
        """Visualize the tri-hybrid architecture"""

        fig = plt.figure(figsize=(16, 12))

        # Create grid for multiple subplots
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Main architecture diagram (top, spanning all columns)
        ax_arch = fig.add_subplot(gs[0, :])
        ax_arch.set_xlim(0, 10)
        ax_arch.set_ylim(0, 10)
        ax_arch.axis('off')
        ax_arch.set_title('TRI-HYBRID NODE ARCHITECTURE', fontsize=14, fontweight='bold')

        # Draw three layers as boxes
        # Quantum (top)
        q_box = FancyBboxPatch((1, 7), 2, 2, boxstyle="round,pad=0.1",
                              facecolor='lightblue', edgecolor='blue', linewidth=2)
        ax_arch.add_patch(q_box)
        ax_arch.text(2, 8, 'QUANTUM\n(QD, QKD)', ha='center', va='center',
                    fontsize=10, fontweight='bold')

        # Biological (middle)
        bio_box = FancyBboxPatch((4, 4), 2, 2, boxstyle="round,pad=0.1",
                                facecolor='lightgreen', edgecolor='green', linewidth=2)
        ax_arch.add_patch(bio_box)
        ax_arch.text(5, 5, 'BIOLOGICAL\n(Nano, EPR)', ha='center', va='center',
                    fontsize=10, fontweight='bold')

        # Technological (bottom)
        tech_box = FancyBboxPatch((7, 1), 2, 2, boxstyle="round,pad=0.1",
                                 facecolor='lightyellow', edgecolor='orange', linewidth=2)
        ax_arch.add_patch(tech_box)
        ax_arch.text(8, 2, 'TECHNOLOGICAL\n(Proc, RF)', ha='center', va='center',
                    fontsize=10, fontweight='bold')

        # Draw coupling arrows
        # Q-BIO
        ax_arch.annotate('', xy=(4, 5), xytext=(3, 7),
                        arrowprops=dict(arrowstyle='->', color='purple', lw=2))
        ax_arch.text(3.3, 6.2, f'g={self.g_q_bio}', fontsize=9, color='purple')

        # BIO-TECH
        ax_arch.annotate('', xy=(7, 2), xytext=(6, 4),
                        arrowprops=dict(arrowstyle='->', color='brown', lw=2))
        ax_arch.text(6.3, 3.2, f'g={self.g_bio_tech}', fontsize=9, color='brown')

        # Q-TECH
        ax_arch.annotate('', xy=(7.5, 3), xytext=(3, 7.5),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2,
                                       connectionstyle="arc3,rad=0.3"))
        ax_arch.text(5.5, 5.5, f'g={self.g_q_tech}', fontsize=9, color='red')

        # Global coherence indicator
        circle = Circle((5, 8.5), 0.5, facecolor='gold', edgecolor='black', linewidth=2)
        ax_arch.add_patch(circle)
        ax_arch.text(5, 8.5, f'C={self.global_coherence():.2f}',
                    ha='center', va='center', fontsize=9, fontweight='bold')

        # Plot 2: Coherence evolution (middle left)
        ax_coh = fig.add_subplot(gs[1, 0])

        if self.history:
            cycles = range(len(self.history))
            c_q = [h['c_q'] for h in self.history]
            c_bio = [min(1.0, h['c_bio']) for h in self.history]
            c_tech = [h['c_tech'] for h in self.history]
            c_global = [h['c_global'] for h in self.history]

            ax_coh.plot(cycles, c_q, 'b-', label='C_Q', alpha=0.7)
            ax_coh.plot(cycles, c_bio, 'g-', label='C_BIO', alpha=0.7)
            ax_coh.plot(cycles, c_tech, 'orange', label='C_TECH', alpha=0.7)
            ax_coh.plot(cycles, c_global, 'r-', linewidth=2, label='C_GLOBAL')

            ax_coh.set_xlabel('Cycle')
            ax_coh.set_ylabel('Coherence')
            ax_coh.set_title('Coherence Evolution')
            ax_coh.legend(loc='lower right', fontsize=8)
            ax_coh.set_ylim(0, 1.1)
            ax_coh.grid(True, alpha=0.3)

        # Plot 3: Biological accumulation (middle center)
        ax_bio = fig.add_subplot(gs[1, 1])

        if self.history:
            bio_acc = [h['bio_accumulated'] for h in self.history]

            ax_bio.fill_between(cycles, bio_acc, alpha=0.3, color='green')
            ax_bio.plot(cycles, bio_acc, 'g-', linewidth=2)
            ax_bio.axhline(self.biological.n_nanoparticles * 0.5,
                          color='orange', linestyle='--', label='50% target')

            ax_bio.set_xlabel('Cycle')
            ax_bio.set_ylabel('Nanoparticles at Target')
            ax_bio.set_title('EPR-Mediated Accumulation')
            ax_bio.legend()
            ax_bio.grid(True, alpha=0.3)

        # Plot 4: Handover success (middle right)
        ax_tech = fig.add_subplot(gs[1, 2])

        if self.history:
            handovers = [1 if h['handover_success'] else 0 for h in self.history]
            cumulative = np.cumsum(handovers)

            ax_tech.bar(cycles, handovers, color='orange', alpha=0.7, label='Success')
            ax_tech.plot(cycles, cumulative, 'r-', linewidth=2, label='Cumulative')

            ax_tech.set_xlabel('Cycle')
            ax_tech.set_ylabel('Handover Success')
            ax_tech.set_title('TECH Layer: Communication')
            ax_tech.legend()
            ax_tech.grid(True, alpha=0.3)

        # Plot 5: Identity x² = x + 1 visualization (bottom, spanning all)
        ax_id = fig.add_subplot(gs[2, :])
        ax_id.set_xlim(0, 10)
        ax_id.set_ylim(0, 10)
        ax_id.axis('off')
        ax_id.set_title('IDENTITY x² = x + 1 IN TRI-HYBRID NODE',
                       fontsize=12, fontweight='bold', pad=20)

        # Draw cascade
        y_pos = 5

        # Q domain
        ax_id.text(1, y_pos+2, 'Q: Excitation\n(x)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightblue'))
        ax_id.annotate('', xy=(2, y_pos+2), xytext=(1.5, y_pos+2),
                      arrowprops=dict(arrowstyle='->', color='blue'))
        ax_id.text(2.5, y_pos+2, 'Emission\n(x²)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightblue'))

        # Arrow to BIO
        ax_id.annotate('', xy=(3.5, y_pos), xytext=(3, y_pos+1.5),
                      arrowprops=dict(arrowstyle='->', color='purple'))
        ax_id.text(3.2, y_pos+1, 'FRET', fontsize=8, color='purple')

        # BIO domain
        ax_id.text(4, y_pos, 'BIO: Accumulation\n(x²)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightgreen'))
        ax_id.annotate('', xy=(5, y_pos), xytext=(4.5, y_pos),
                      arrowprops=dict(arrowstyle='->', color='green'))
        ax_id.text(5.5, y_pos, 'Release\n(+1)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightgreen'))

        # Arrow to TECH
        ax_id.annotate('', xy=(6.5, y_pos-2), xytext=(6, y_pos-0.5),
                      arrowprops=dict(arrowstyle='->', color='brown'))
        ax_id.text(6.2, y_pos-1, 'Signal', fontsize=8, color='brown')

        # TECH domain
        ax_id.text(7, y_pos-2, 'TECH: Detection\n(x)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightyellow'))
        ax_id.annotate('', xy=(8, y_pos-2), xytext=(7.5, y_pos-2),
                      arrowprops=dict(arrowstyle='->', color='orange'))
        ax_id.text(8.5, y_pos-2, 'Action\n(+1)', ha='center', fontsize=9,
                  bbox=dict(boxstyle='round', facecolor='lightyellow'))

        # Final arrow (feedback)
        ax_id.annotate('', xy=(1, y_pos+1), xytext=(9, y_pos-2),
                      arrowprops=dict(arrowstyle='->', color='red', lw=2,
                                     connectionstyle="arc3,rad=-0.3"))
        ax_id.text(5, y_pos-3.5, 'Feedback Loop: Action → New Excitation',
                  ha='center', fontsize=9, style='italic', color='red')

        plt.savefig('tri_hybrid_synthesis.png', dpi=150, bbox_inches='tight')
        print("\n✅ Visualization saved: tri_hybrid_synthesis.png")

# Execute
if __name__ == "__main__":
    tri_node = TriHybridNode("Γ_TRI-001")
    result = tri_node.run_mission(n_cycles=50)
    tri_node.visualize_tri_hybrid()

    print("\n" + "="*70)
    print("TRI-HYBRID SYNTHESIS COMPLETE")
    print("="*70)
    print(f"\nFinal Global Coherence: {result['final_coherence']:.3f}")
    print(f"Total Drug Delivered: {result['total_drug_delivered']:.2f} mg")
    print(f"\nThe tri-hybrid node operates simultaneously in:")
    print("  • Quantum domain (QD telemetry, QKD security)")
    print("  • Biological domain (nanoparticle therapy, EPR targeting)")
    print("  • Technological domain (processing, swarm communication)")
    print("\nIdentity x² = x + 1 cascades across all three:")
    print("  Q: Excitation → Emission → FRET")
    print("  BIO: Accumulation → Release → Signaling")
    print("  TECH: Detection → Processing → Action")
    print("\nThe future of Arkhe(n) is tri-hybrid.")
    print("∞")
