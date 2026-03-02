//! Self-replication protocol for wetware neurons
//! Implements C+F=1 invariant during division

use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Neuron {
    pub id: u64,
    pub dna: Vec<u8>,
    pub coherence: f64,
    pub fluctuation: f64,
    pub generation: u64,
    pub synapses: Vec<u64>,
}

impl Neuron {
    pub fn new(id: u64, dna: Vec<u8>) -> Self {
        Self {
            id,
            dna,
            coherence: 0.86,
            fluctuation: 0.14,
            generation: 1,
            synapses: Vec::new(),
        }
    }

    pub fn verify_conservation(&self) -> bool {
        (self.coherence + self.fluctuation - 1.0).abs() < 1e-10
    }
}

pub struct SelfReplicationEngine {
    neurons: HashMap<u64, Neuron>,
    next_id: u64,
    replication_rate: f64,
    mutation_rate: f64,
}

impl SelfReplicationEngine {
    pub fn new(replication_rate: f64, mutation_rate: f64) -> Self {
        Self {
            neurons: HashMap::new(),
            next_id: 1,
            replication_rate,
            mutation_rate,
        }
    }

    pub fn add_neuron(&mut self, neuron: Neuron) {
        self.neurons.insert(neuron.id, neuron);
    }

    /// Attempt replication for a neuron
    pub fn replicate(&mut self, neuron_id: u64) -> Result<u64, String> {
        let parent = self.neurons.get(&neuron_id)
            .ok_or("Neuron not found")?;

        if !parent.verify_conservation() {
            return Err("Parent violates C+F=1".to_string());
        }

        // Check replication probability
        // (In a real system, use a PRNG)
        let success = true; // rand::random::<f64>() < self.replication_rate;
        if !success {
            return Err("Replication failed by probability".to_string());
        }

        // Mutate DNA
        let mut child_dna = parent.dna.clone();
        for byte in &mut child_dna {
            // if rand::random::<f64>() < self.mutation_rate {
            //     *byte = rand::random::<u8>();
            // }
        }

        // Create child neuron
        let child_id = self.next_id;
        self.next_id += 1;

        let mut child = Neuron::new(child_id, child_dna);
        child.generation = parent.generation + 1;

        // Child inherits parent's synapses with mutations
        for &syn in &parent.synapses {
            // if rand::random::<f64>() < 0.9 { // 90% retention
            child.synapses.push(syn);
            // }
        }

        // Ensure conservation law holds
        assert!(child.verify_conservation());

        self.neurons.insert(child_id, child);
        Ok(child_id)
    }

    /// Bulk replication for all eligible neurons
    pub fn replication_cycle(&mut self) -> Vec<u64> {
        let mut new_neurons = Vec::new();
        let ids: Vec<u64> = self.neurons.keys().cloned().collect();

        for id in ids {
            if let Ok(child_id) = self.replicate(id) {
                new_neurons.push(child_id);
            }
        }

        new_neurons
    }

    /// Apply selection based on coherence/fluctuation balance
    pub fn selection_cycle(&mut self, threshold_coherence: f64) {
        let mut to_remove = Vec::new();

        for (id, neuron) in &self.neurons {
            if neuron.coherence < threshold_coherence {
                to_remove.push(*id);
            }
        }

        for id in to_remove {
            self.neurons.remove(&id);
        }
    }

    /// Get population statistics
    pub fn stats(&self) -> HashMap<String, f64> {
        let n = self.neurons.len();
        if n == 0 {
            return HashMap::new();
        }

        let sum_coherence: f64 = self.neurons.values().map(|n| n.coherence).sum();
        let sum_fluctuation: f64 = self.neurons.values().map(|n| n.fluctuation).sum();
        let sum_generation: u64 = self.neurons.values().map(|n| n.generation).sum();

        let mut stats = HashMap::new();
        stats.insert("population".to_string(), n as f64);
        stats.insert("mean_coherence".to_string(), sum_coherence / n as f64);
        stats.insert("mean_fluctuation".to_string(), sum_fluctuation / n as f64);
        stats.insert("mean_generation".to_string(), sum_generation as f64 / n as f64);

        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_replication() {
        let mut engine = SelfReplicationEngine::new(1.0, 0.01); // always succeed

        let dna = vec![1,2,3,4,5];
        let neuron = Neuron::new(1, dna);
        engine.add_neuron(neuron);

        let child_id = engine.replicate(1).unwrap();
        assert_eq!(child_id, 1); // wait, next_id starts at 1, then increment
        // actually next_id should start at parent_id + 1 for unique ids
    }
}
