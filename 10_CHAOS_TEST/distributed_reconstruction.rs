//! Distributed Reconstruction During Chaos
//! Combines four mechanisms with dynamic weights

use ndarray::{Array1, Array2};
// use rand::Rng;

#[derive(Clone)]
pub struct ReconstructionState {
    pub kalman_weight: f64,
    pub grad_weight: f64,
    pub phase_weight: f64,
    pub constraint_weight: f64,
}

impl ReconstructionState {
    pub fn new() -> Self {
        Self {
            kalman_weight: 0.40,
            grad_weight: 0.20,
            phase_weight: 0.30,
            constraint_weight: 0.10,
        }
    }

    pub fn total(&self) -> f64 {
        self.kalman_weight + self.grad_weight + self.phase_weight + self.constraint_weight
    }
}

pub struct DistributedReconstructor {
    n_nodes: usize,
    adjacency: Array2<f64>,
    state: ReconstructionState,
}

impl DistributedReconstructor {
    pub fn new(n_nodes: usize, connectivity: f64) -> Self {
        // Create random adjacency matrix (undirected, sparse)
        let mut adj = Array2::<f64>::zeros((n_nodes, n_nodes));
        // let mut rng = rand::thread_rng();

        for i in 0..n_nodes {
            for j in i+1..n_nodes {
                // if rng.gen::<f64>() < connectivity {
                //     let weight = rng.gen_range(0.1..1.0);
                //     adj[[i, j]] = weight;
                //     adj[[j, i]] = weight;
                // }
            }
        }

        Self {
            n_nodes,
            adjacency: adj,
            state: ReconstructionState::new(),
        }
    }

    /// Kalman prediction (temporal)
    pub fn kalman_predict(&self, prev_syzygy: &Array1<f64>, node: usize) -> f64 {
        // Simple linear prediction based on past values
        if node >= prev_syzygy.len() { return 0.86; }
        prev_syzygy[node] // + 0.001 * rand::random::<f64>()
    }

    /// Gradient continuity (spatial)
    pub fn gradient_estimate(&self, syzygy: &Array1<f64>, node: usize) -> f64 {
        // Interpolate from neighbors
        let mut sum = 0.0;
        let mut count = 0;

        for j in 0..self.n_nodes {
            if j != node && self.adjacency[[node, j]] > 0.0 {
                sum += syzygy[j];
                count += 1;
            }
        }

        if count > 0 { sum / count as f64 } else { 0.86 }
    }

    /// Phase alignment (⟨0.00|0.07⟩ = 0.94)
    pub fn phase_alignment(&self) -> f64 {
        0.94  // constant from Arkhe invariant
    }

    /// Global C+F=1 constraint
    pub fn global_constraint(&self) -> f64 {
        0.86  // forces coherence back to optimal
    }

    /// Reconstruct a single node
    pub fn reconstruct_node(&self,
                          prev_syzygy: &Array1<f64>,
                          syzygy: &Array1<f64>,
                          node: usize) -> f64 {

        let kalman = self.kalman_predict(prev_syzygy, node);
        let grad = self.gradient_estimate(syzygy, node);
        let phase = self.phase_alignment();
        let constraint = self.global_constraint();

        self.state.kalman_weight * kalman +
        self.state.grad_weight * grad +
        self.state.phase_weight * phase +
        self.state.constraint_weight * constraint
    }

    /// Reconstruct all gap nodes
    pub fn reconstruct_gap(&mut self,
                          prev_syzygy: &Array1<f64>,
                          syzygy: &Array1<f64>,
                          gap_nodes: &[usize]) -> Array1<f64> {

        let mut reconstructed = Array1::<f64>::zeros(gap_nodes.len());

        for (i, &node) in gap_nodes.iter().enumerate() {
            reconstructed[i] = self.reconstruct_node(prev_syzygy, syzygy, node);
        }

        reconstructed
    }

    /// Compute reconstruction fidelity
    pub fn fidelity(&self, reconstructed: &Array1<f64>, ground_truth: &Array1<f64>) -> f64 {
        let mut error_sum = 0.0;
        for i in 0..reconstructed.len() {
            let err = (reconstructed[i] - ground_truth[i]).abs();
            error_sum += err / ground_truth[i];
        }
        1.0 - error_sum / reconstructed.len() as f64
    }
}
