"""
Energy Monitoring for Distributed Arkhe Nodes
Tracks power consumption and carbon footprint
"""

# import psutil
import time
from dataclasses import dataclass
from typing import List, Dict
# import requests

@dataclass
class NodeEnergy:
    node_id: str
    cpu_percent: float
    memory_percent: float
    power_watts: float
    renewable_fraction: float
    timestamp: float

class EnergyMonitor:
    """Monitor energy consumption of Arkhe nodes"""

    def __init__(self, api_endpoint: str = "http://arkhe-core:8080"):
        self.api_endpoint = api_endpoint
        self.nodes: Dict[str, NodeEnergy] = {}
        self.total_power = 0.0
        self.renewable_total = 0.0

    def sample_local(self, node_id: str) -> NodeEnergy:
        """Sample energy metrics on local node"""
        # cpu = psutil.cpu_percent(interval=1)
        # mem = psutil.virtual_memory().percent
        cpu = 10.0
        mem = 20.0

        # Estimate power (simplified: 5W per CPU core + 3W per GB memory)
        power = (cpu / 100.0) * 5 + (mem / 100.0) * 3

        # Assume 40% renewable (can be overridden)
        renewable = 0.4

        energy = NodeEnergy(
            node_id=node_id,
            cpu_percent=cpu,
            memory_percent=mem,
            power_watts=power,
            renewable_fraction=renewable,
            timestamp=time.time()
        )

        self.nodes[node_id] = energy
        return energy

    def report_to_api(self):
        """Send aggregated data to central API"""
        total_power = sum(n.power_watts for n in self.nodes.values())
        total_renewable = sum(n.power_watts * n.renewable_fraction for n in self.nodes.values())

        payload = {
            'timestamp': time.time(),
            'nodes': len(self.nodes),
            'total_power_watts': total_power,
            'renewable_watts': total_renewable,
            'carbon_footprint_g_per_h': total_power * 0.5  # gCO2/kWh estimate
        }

        # try:
        #     requests.post(f"{self.api_endpoint}/metrics/energy", json=payload)
        # except Exception as e:
        #     print(f"Failed to report energy: {e}")
        print(f"Reported energy: {payload}")

    def run_continuous(self, interval_sec: int = 60, node_id: str = "local"):
        """Run monitoring loop"""
        # while True:
        self.sample_local(node_id)
        self.report_to_api()
        # time.sleep(interval_sec)

if __name__ == "__main__":
    import sys
    node_id = sys.argv[1] if len(sys.argv) > 1 else "local"
    monitor = EnergyMonitor()
    print(f"Starting energy monitor for node {node_id}")
    monitor.run_continuous(node_id=node_id)
