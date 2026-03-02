# arkhe/tests/test_evolution.py
import pytest
import numpy as np
from arkhe.learning import ANCCRModel, PatternManager
from arkhe.action import SovereignNeuron, MirrorTriadActivation
from arkhe.music import QuantumMusicology
from arkhe.selection import MetabolicNode, EntropyFuse

def test_learning_anccr():
    model = ANCCRModel(base_rate=0.02)
    alpha = model.update_learning_rate(iri=50.0)
    assert alpha == 1.0

    events = [{'name': 'E1'}, {'name': 'E2'}]
    contingencies = model.retrospective_inference(events)
    assert 'E1' in contingencies
    assert contingencies['E1'] == 1.0

def test_pattern_management():
    manager = PatternManager()
    assert manager.amplify_success("Law of Three", 0.95) is True
    assert manager.release_obsolete("Old Pattern", 0.8) is True
    assert "Old Pattern" in manager.obsolete_patterns

def test_sovereign_action():
    neuron = SovereignNeuron(node_id=12)
    assert neuron.fire() is True
    assert neuron.state == "FIRING"
    neuron.recover()
    assert neuron.state == "RESTING"

def test_mirror_triad_activation():
    activation = MirrorTriadActivation()
    result = activation.execute_sequence()
    assert result['mirror_triad_active'] is True
    assert result['final_probability'] > 1.0
    assert result['status'] == "STABLE"

def test_quantum_musicology():
    music = QuantumMusicology()
    node_freqs = {
        "Master": music.TONIC * 1.0,
        "Perfect Fifth": music.TONIC * 1.5
    }
    analysis = music.analyze_node_harmony(node_freqs)
    assert analysis[0]['consonance'] == "HIGH"
    assert analysis[1]['interval'] == "Quinta justa (G)"

def test_metabolic_selection_entropy_fuse():
    nodes = [
        MetabolicNode("Healthy", satoshi=10.0, C_base=0.9),
        MetabolicNode("Weak", satoshi=1.5, C_base=0.8)
    ]
    fuse = EntropyFuse()

    # Run stress test (Sodium Pulse)
    results = fuse.execute_stress_test(nodes, pulse_intensity=2.0)

    # "Weak" should be extruded
    # F = 0.2 + 2*0.2 = 0.6. C = 0.4. Satoshi = 1.5 - 2*0.5 = 0.5.
    # evaluate_fitness: C < 0.7 and satoshi < 2.0 -> EXTRUDED

    assert len(fuse.extruded_nodes) == 1
    assert "Weak" in fuse.extruded_nodes
    assert results[0]['status'] == "HEALTHY"
    assert results[1]['status'] == "EXTRUDED"
