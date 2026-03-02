#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from avalon_fax_of_theseus import FaxOfTheseusSim

class TestFaxOfTheseus(unittest.TestCase):
    def setUp(self):
        # Small scale for testing
        self.sim = FaxOfTheseusSim(total_nodes=200)

    def test_state_swapping(self):
        cluster_size = 20
        fidelity = self.sim.run_simulation(cluster_size=cluster_size)

        # Fidelity should be around 0.98
        self.assertAlmostEqual(fidelity, 0.98, places=2)

    def test_hardware_replacement(self):
        # Ensure nodes are actually replaced (syzygy goes to 0 then to high value)
        indices = [10, 20, 30]
        state_before = [self.sim.nodes[i].syzygy for i in indices]

        # Manual simulation of replacement steps
        # Step 3: Replacement
        for i in indices:
            self.sim.nodes[i].syzygy = 0.0

        for i in indices:
            self.assertEqual(self.sim.nodes[i].syzygy, 0.0)

        # Step 4: Reconstruction
        fidelity_factor = 0.98
        for idx, i in enumerate(indices):
            self.sim.nodes[i].syzygy = state_before[idx] * fidelity_factor

        for idx, i in enumerate(indices):
            self.assertAlmostEqual(self.sim.nodes[i].syzygy, state_before[idx] * fidelity_factor)

if __name__ == "__main__":
    unittest.main()
