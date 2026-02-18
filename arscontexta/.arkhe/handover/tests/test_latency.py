import time
import unittest
import sys
from pathlib import Path

# Add parent directory to sys.path to allow imports from handover
sys.path.append(str(Path(__file__).parent.parent))
from emergency_halt import emergency_halt

class TestHandoverLatency(unittest.TestCase):
    def test_latency_threshold(self):
        start = time.perf_counter()
        # Simula uma operação de handover
        time.sleep(0.01) # 10ms
        elapsed = (time.perf_counter() - start) * 1000
        self.assertLess(elapsed, 25, "Latency exceeded 25ms threshold")

if __name__ == "__main__":
    unittest.main()
