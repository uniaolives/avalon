use crate::arkhe_core::{Node, Handover};
use std::time::{SystemTime, UNIX_EPOCH};

pub fn compute_handover_strength(from: &Node, to: &Node, alpha: f64) -> f64 {
    let distance = match (from.position, to.position) {
        (Some(p1), Some(p2)) => {
            let dx = p1.0 - p2.0;
            let dy = p1.1 - p2.1;
            let dz = p1.2 - p2.2;
            (dx*dx + dy*dy + dz*dz).sqrt()
        },
        _ => 1.0, // distância padrão se não houver posição
    };
    let distance_term = if distance > 0.0 { 1.0 / distance.powf(alpha) } else { 1.0 };
    let coherence_product = from.coherence * to.coherence;
    let phase_term = (from.phase - to.phase).cos();
    coherence_product * distance_term * phase_term
}

pub fn execute_handover(from: &mut Node, to: &mut Node, payload: Vec<u8>,
                         base_cost: f64) -> Result<Handover, String> {
    if from.satoshi < base_cost {
        return Err(format!("Nó {} sem satoshi suficiente", from.id));
    }
    let strength = compute_handover_strength(from, to, 2.0); // α=2 para RF
    let cost = base_cost * (1.0 + strength * 0.5); // custo ajustado pela força
    from.satoshi -= cost;
    to.satoshi += cost * 0.1; // 10% de recompensa para o receptor

    from.update_coherence(0.01 * strength);
    to.update_coherence(0.005 * strength);

    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis() as u64;

    Ok(Handover {
        from: from.id,
        to: to.id,
        timestamp,
        strength,
        payload,
        cost,
    })
}
