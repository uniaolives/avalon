use serde::{Serialize, Deserialize};
use std::collections::HashMap;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Node {
    pub id: u64,
    pub node_type: NodeType,
    pub satoshi: f64,          // memória acumulada
    pub coherence: f64,        // C
    pub fluctuation: f64,      // F
    pub phase: f64,            // θ (radianos)
    pub position: Option<(f64, f64, f64)>, // coordenadas 3D opcionais
    pub metadata: HashMap<String, String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum NodeType {
    Drone,
    BioSensor,
    NanoLaser,
    GLPMeta,
    BaseStation,
    Simulated,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Handover {
    pub from: u64,
    pub to: u64,
    pub timestamp: u64,        // ms desde época
    pub strength: f64,         // intensidade do handover
    pub payload: Vec<u8>,      // dados transmitidos
    pub cost: f64,             // satoshi gasto
}

impl Node {
    pub fn new(id: u64, node_type: NodeType) -> Self {
        Node {
            id,
            node_type,
            satoshi: 10.0,
            coherence: 0.9,
            fluctuation: 0.1,
            phase: 0.0,
            position: None,
            metadata: HashMap::new(),
        }
    }

    pub fn update_coherence(&mut self, delta: f64) {
        self.coherence += delta;
        if self.coherence > 1.0 { self.coherence = 1.0; }
        if self.coherence < 0.0 { self.coherence = 0.0; }
        self.fluctuation = 1.0 - self.coherence;
    }

    pub fn can_handover(&self, target: &Node, min_coherence: f64) -> bool {
        self.coherence >= min_coherence && target.coherence >= min_coherence
    }
}
