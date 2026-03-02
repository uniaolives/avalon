# test_rfid.py
import numpy as np
from datetime import datetime, timedelta
from arkhe.rfid import RFIDTag, RFIDHypergraph

def test_rfid_simulation():
    hypergraph = RFIDHypergraph()

    tag1 = RFIDTag("RFID_001", "smartphone")
    tag2 = RFIDTag("RFID_002", "tablet")

    hypergraph.add_tag(tag1)
    hypergraph.add_tag(tag2)

    start_time = datetime.now()

    # Simular leituras regulares para tag1 (Alta coerência)
    for i in range(5):
        t = start_time + timedelta(seconds=i*3600)
        hypergraph.register_reading("RFID_001", f"reader_{i}", f"location_{i}", t)

    # Simular leituras irregulares para tag2 (Baixa coerência)
    intervals = [10, 3600, 7200, 100]
    curr_time = start_time
    for i, delta in enumerate(intervals):
        curr_time += timedelta(seconds=delta)
        hypergraph.register_reading("RFID_002", f"reader_x", "location_y", curr_time)

    c1 = tag1.coherence_history[-1]['C']
    c2 = tag2.coherence_history[-1]['C']

    print(f"Tag 1 Coherence: {c1:.4f}")
    print(f"Tag 2 Coherence: {c2:.4f}")
    print(f"System Coherence: {hypergraph.compute_system_coherence():.4f}")
    print(f"Tag 1 C+F=1? {tag1.verify_conservation()}")
    print(f"Tag 2 C+F=1? {tag2.verify_conservation()}")

    assert c1 > c2, "Tag 1 should be more coherent than Tag 2"
    assert tag1.verify_conservation(), "C+F=1 failed for Tag 1"
    assert tag2.verify_conservation(), "C+F=1 failed for Tag 2"
    print("✅ RFID Simulation Test Passed")

if __name__ == "__main__":
    test_rfid_simulation()
