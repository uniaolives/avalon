"""
Wetware Neural Network Simulation
10,000 neuron model with genetic feedback and optogenetic control
"""

import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Neuron:
    """Single neuron model with state and plasticity"""
    id: int
    x: float
    y: float
    z: float
    membrane_potential: float = -70.0  # mV
    firing_rate: float = 0.0  # Hz
    syzygy: float = 0.0  # Local coherence
    opsins: List[str] = None  # Expressed opsins

    def __post_init__(self):
        if self.opsins is None:
            self.opsins = []

class Synapse:
    """Connection between neurons"""
    def __init__(self, pre: int, post: int, weight: float = 0.5):
        self.pre = pre
        self.post = post
        self.weight = weight
        self.plasticity = 1.0
        self.handover_count = 0

class WetwareNetwork:
    """
    3D neural network with optogenetic control and self-replication
    """

    def __init__(self,
                 n_neurons: int = 10000,
                 grid_size: Tuple[float, float, float] = (100.0, 100.0, 100.0)):

        self.n_neurons = n_neurons
        self.grid_size = grid_size
        self.neurons: List[Neuron] = []
        self.synapses: List[Synapse] = []
        self.opsin_library = {}  # name -> spectral sensitivity
        self.generation = 1
        self.syzygy_history = []

        # Initialize neurons in 3D grid
        self._initialize_neurons()
        self._initialize_connections()

    def _initialize_neurons(self):
        """Distribute neurons randomly in 3D volume"""
        for i in range(self.n_neurons):
            x = np.random.uniform(0, self.grid_size[0])
            y = np.random.uniform(0, self.grid_size[1])
            z = np.random.uniform(0, self.grid_size[2])

            # Initial opsins (some neurons start with baseline)
            opsins = ['ChR2'] if np.random.random() < 0.1 else []

            neuron = Neuron(
                id=i,
                x=x, y=y, z=z,
                membrane_potential=-70.0 + np.random.randn() * 5,
                firing_rate=0.0,
                opsins=opsins
            )
            self.neurons.append(neuron)

    def _initialize_connections(self, connection_prob: float = 0.01):
        """Create random synaptic connections"""
        for i in range(self.n_neurons):
            for j in range(self.n_neurons):
                if i == j:
                    continue
                if np.random.random() < connection_prob:
                    weight = np.random.uniform(0.1, 1.0)
                    self.synapses.append(Synapse(i, j, weight))

    def load_opsin_library(self, library: Dict[str, Dict]):
        """Load spectral sensitivity data for opsins"""
        self.opsin_library = library

    def stimulate_light(self, frequency: float, intensity: float = 1.0):
        """
        Apply optogenetic stimulation at given frequency (Hz)
        Neurons with opsins sensitive to this frequency depolarize
        """
        # Find opsins sensitive to this frequency (simplified)
        sensitive_neurons = []
        for i, neuron in enumerate(self.neurons):
            for opsin in neuron.opsins:
                if opsin in self.opsin_library:
                    # Check if frequency is within sensitivity range
                    sens = self.opsin_library[opsin]
                    if sens['min_freq'] <= frequency <= sens['max_freq']:
                        # Depolarize
                        neuron.membrane_potential += intensity * 5.0
                        sensitive_neurons.append(i)
                        break

        return sensitive_neurons

    def step(self, dt: float = 0.001):
        """
        Single simulation step
        - Update membrane potentials (leaky integrate-and-fire)
        - Spike propagation
        - Handover counting
        """
        # Spike detection
        spikes = []
        for i, neuron in enumerate(self.neurons):
            if neuron.membrane_potential > -55:  # Threshold
                neuron.firing_rate = 100.0  # Hz
                neuron.membrane_potential = -70.0  # Reset
                spikes.append(i)
            else:
                # Leak
                neuron.membrane_potential -= 0.1
                neuron.firing_rate *= 0.9

        # Synaptic transmission
        for synapse in self.synapses:
            if synapse.pre in spikes:
                # Increase postsynaptic potential
                self.neurons[synapse.post].membrane_potential += synapse.weight * 2.0
                synapse.handover_count += 1
                # Hebbian plasticity
                synapse.weight += 0.001
                if synapse.weight > 1.0:
                    synapse.weight = 1.0

        # Compute syzygy (coherence measure)
        active = [n for n in self.neurons if n.firing_rate > 10]
        self.syzygy = len(active) / self.n_neurons if self.n_neurons > 0 else 0

        return spikes

    def replicate(self) -> 'WetwareNetwork':
        """
        Self-replication: create a daughter network with mutations
        """
        daughter = WetwareNetwork(n_neurons=self.n_neurons)
        daughter.generation = self.generation + 1

        # Copy neurons with mutations
        for i, neuron in enumerate(self.neurons):
            # Inherit opsins with mutation
            opsins = neuron.opsins.copy()
            if np.random.random() < 0.01:  # mutation rate
                # Add random opsin
                if self.opsin_library:
                    new_opsin = np.random.choice(list(self.opsin_library.keys()))
                    opsins.append(new_opsin)
            daughter.neurons[i].opsins = opsins

        # Copy synapses with mutation
        for synapse in self.synapses:
            if np.random.random() < 0.05:  # 5% mutation
                continue  # skip (remove)
            daughter.synapses.append(Synapse(
                synapse.pre, synapse.post,
                min(1.0, synapse.weight * np.random.uniform(0.9, 1.1))
            ))

        return daughter

    def evolve(self, target_frequency: float, generations: int = 10):
        """
        Evolve network by selecting for response to target frequency
        """
        history = []
        for gen in range(generations):
            # Test response
            spikes_before = self.stimulate_light(target_frequency)
            response = len(spikes_before)

            # Replicate
            daughter = self.replicate()

            # Test daughter
            spikes_daughter = daughter.stimulate_light(target_frequency)
            response_daughter = len(spikes_daughter)

            # Select better
            if response_daughter > response:
                self = daughter
                print(f"Gen {gen}: improved response {response} → {response_daughter}")
            else:
                print(f"Gen {gen}: response {response} (no improvement)")

            history.append(max(response, response_daughter))

        return history

    def compute_memory(self) -> float:
        """
        Estimate memory capacity via synaptic weights
        """
        total_weight = sum(s.weight for s in self.synapses)
        return total_weight / len(self.synapses) if self.synapses else 0

    def plot_activity(self):
        """Plot firing rates and connectivity"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Firing rates
        rates = [n.firing_rate for n in self.neurons]
        axes[0,0].hist(rates, bins=50)
        axes[0,0].set_xlabel('Firing rate (Hz)')
        axes[0,0].set_ylabel('Neurons')
        axes[0,0].set_title('Firing Rate Distribution')

        # Synaptic weights
        weights = [s.weight for s in self.synapses]
        axes[0,1].hist(weights, bins=50)
        axes[0,1].set_xlabel('Synaptic weight')
        axes[0,1].set_ylabel('Count')
        axes[0,1].set_title('Synaptic Weight Distribution')

        # 3D scatter of neurons colored by opsin type
        colors = {'ChR2': 'blue', 'NpHR': 'red', 'Arch': 'green', 'VChR1': 'purple'}
        for neuron in self.neurons:
            if neuron.opsins:
                opsin = neuron.opsins[0]
                color = colors.get(opsin, 'gray')
                axes[1,0].scatter(neuron.x, neuron.y, c=color, alpha=0.5, s=10)
        axes[1,0].set_xlabel('X')
        axes[1,0].set_ylabel('Y')
        axes[1,0].set_title('Neuron Positions (colored by opsin)')

        # Syzygy over time if history exists
        if self.syzygy_history:
            axes[1,1].plot(self.syzygy_history)
            axes[1,1].set_xlabel('Step')
            axes[1,1].set_ylabel('Syzygy')
            axes[1,1].set_title('Network Coherence')

        plt.tight_layout()
        plt.savefig('wetware_activity.png')
        print("Plot saved to wetware_activity.png")

# Example usage
def example_wetware():
    """Create and simulate a wetware network"""

    net = WetwareNetwork(n_neurons=1000)

    # Load opsin library
    net.load_opsin_library({
        'ChR2': {'min_freq': 470e12, 'max_freq': 495e12},  # blue light
        'NpHR': {'min_freq': 580e12, 'max_freq': 620e12},  # yellow light
        'Arch': {'min_freq': 550e12, 'max_freq': 570e12},  # green light
        'VChR1': {'min_freq': 500e12, 'max_freq': 530e12}, # cyan light
    })

    # Simulate for 1000 steps
    for step in range(1000):
        spikes = net.step()
        net.syzygy_history.append(net.syzygy)
        if step % 200 == 0:
            print(f"Step {step}: {len(spikes)} spikes, syzygy={net.syzygy:.3f}")

    # Plot results
    net.plot_activity()

    return net

if __name__ == "__main__":
    example_wetware()
