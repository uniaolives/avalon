use crate::arkhe_core::Node;

pub struct DroneNode {
    pub node: Node,
    pub mission_progress: f64,   // 0..1
    pub target_position: (f64, f64, f64),
}

impl DroneNode {
    pub fn new(id: u64, initial_pos: (f64, f64, f64)) -> Self {
        let mut node = Node::new(id, crate::arkhe_core::NodeType::Drone);
        node.position = Some(initial_pos);
        DroneNode {
            node,
            mission_progress: 0.0,
            target_position: (0.0, 0.0, 0.0),
        }
    }

    pub fn fly_towards_target(&mut self, dt: f64) {
        if let Some(pos) = self.node.position {
            let dx = self.target_position.0 - pos.0;
            let dy = self.target_position.1 - pos.1;
            let dz = self.target_position.2 - pos.2;
            let dist = (dx*dx + dy*dy + dz*dz).sqrt();
            if dist > 0.1 {
                let speed = 1.0; // m/s
                let step = speed * dt;
                let ratio = step / dist;
                let new_x = pos.0 + dx * ratio.min(1.0);
                let new_y = pos.1 + dy * ratio.min(1.0);
                let new_z = pos.2 + dz * ratio.min(1.0);
                self.node.position = Some((new_x, new_y, new_z));
                // Consome satoshi para movimento
                self.node.satoshi -= 0.01 * dt;
            }
        }
    }

    pub fn sense(&self) -> Vec<f64> {
        // Simulação de leitura de sensores (IMU, câmera, etc.)
        let mut readings = Vec::new();
        // Exemplo: gerar um vetor com ruído
        for _ in 0..6 {
            readings.push(rand::random::<f64>());
        }
        readings
    }

    pub fn process(&mut self, sensor_data: Vec<f64>) -> f64 {
        // Processamento local (ex.: Kalman, gradiente) – simulação
        let processed = sensor_data.iter().sum::<f64>() / sensor_data.len() as f64;
        // Auto‑acoplamento: atualiza coerência baseado no processamento
        self.node.coherence += 0.02 * processed;
        self.node.coherence = self.node.coherence.min(1.0).max(0.0);
        self.node.fluctuation = 1.0 - self.node.coherence;
        processed
    }

    pub fn act(&mut self, processed: f64) {
        // Decisão baseada no processamento
        if processed > 0.5 {
            self.mission_progress += 0.01;
        }
        self.node.satoshi += 0.001; // pequena recompensa por ação
    }
}
