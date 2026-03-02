#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from avalon_teleport_lysosome import QuantumNode, AvalonTeleportSim

class TestTeleportLysosome(unittest.TestCase):
    def setUp(self):
        self.sim = AvalonTeleportSim()

    def test_quantum_teleport_state(self):
        source = QuantumNode("Source", syzygy=1.0, hesitation=0.0, omega=0.0)
        destination = QuantumNode("Destination", syzygy=0.0, hesitation=0.1, omega=0.1)

        self.sim.quantum_teleport_state(source, destination)

        # Source should be destroyed
        self.assertEqual(source.syzygy, 0.0)
        # Destination should have reconstructed state (with 0.98 fidelity)
        self.assertAlmostEqual(destination.syzygy, 0.98)

    def test_lysosomal_cleaning(self):
        node = QuantumNode("DirtyNode", syzygy=0.5, hesitation=0.2, omega=0.1)

        initial_hesitation = node.hesitation
        initial_syzygy = node.syzygy

        self.sim.lysosomal_cleaning(node)

        # Hesitation should decrease
        self.assertLess(node.hesitation, initial_hesitation)
        self.assertAlmostEqual(node.hesitation, initial_hesitation * 0.2) # 80% reduction

        # Syzygy should increase
        self.assertGreater(node.syzygy, initial_syzygy)

    def test_simulation_run(self):
        # Just ensure it runs without error
        try:
            self.sim.run_simulation()
        except Exception as e:
            self.fail(f"run_simulation raised {type(e).__name__} unexpectedly!")

if __name__ == "__main__":
    unittest.main()
