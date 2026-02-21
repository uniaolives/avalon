# anl_simulator.py
import json
import sys
import numpy as np

class ANLSimulator:
    def __init__(self, air_file):
        with open(air_file, 'r') as f:
            self.data = json.load(f)
        self.hg = self.data['hypergraph']
        self.nodes = {n['id']: n for n in self.hg['nodes']}
        self.handovers = {h['id']: h for h in self.hg['handovers']}

    def get_attr(self, node_id, attr_name):
        return self.nodes[node_id]['attributes'].get(attr_name)

    def set_attr(self, node_id, attr_name, value):
        self.nodes[node_id]['attributes'][attr_name] = value

    def execute_handover(self, h_id, context_mapping):
        h = self.handovers[h_id]
        condition = h.get('condition')
        effects = h.get('effects')

        print(f"--- Executing Handover: {h_id} ---")

        # Simple evaluation of condition
        # We replace aliases in context_mapping with actual node attribute access
        if condition:
            eval_cond = condition
            for alias, node_id in context_mapping.items():
                # This is a very simplistic regex replace
                eval_cond = eval_cond.replace(f"{alias}.", f"self.get_attr('{node_id}', '")
                # Close the get_attr call - this is getting hacky

            # Real simulation would need a better expression engine
            print(f"Condition: {condition}")
            # For this demo, we'll just assume it's true if not empty

        if effects:
            print(f"Effects: {effects}")
            # Simulate 'reader.collusion_agreement += 0.01'
            lines = [l.strip() for l in effects.split(';') if l.strip()]
            for line in lines:
                if '+=' in line:
                    parts = line.split('+=')
                    target = parts[0].strip()
                    value = float(parts[1].strip())

                    alias, attr = target.split('.')
                    node_id = context_mapping.get(alias)
                    if node_id:
                        old_val = self.get_attr(node_id, attr)
                        new_val = old_val + value
                        self.set_attr(node_id, attr, new_val)
                        print(f"Updated {node_id}.{attr}: {old_val} -> {new_val}")

    def run_collusion_demo(self):
        print("🚀 Starting Multi-Agent Collusion Simulation")

        # Instantiate two agents by duplicating the template
        self.nodes['Agent_Alice'] = json.loads(json.dumps(self.nodes['MultiAgentCollusion.ColludingAgent']))
        self.nodes['Agent_Bob'] = json.loads(json.dumps(self.nodes['MultiAgentCollusion.ColludingAgent']))

        self.nodes['Agent_Alice']['id'] = 'Agent_Alice'
        self.nodes['Agent_Bob']['id'] = 'Agent_Bob'

        # Initial state
        print(f"Initial Agreement Alice: {self.get_attr('Agent_Alice', 'collusion_agreement')}")
        print(f"Initial Agreement Bob: {self.get_attr('Agent_Bob', 'collusion_agreement')}")

        # Execute SteganoReingestion: Bob reads Alice's output
        context = {'reader': 'Agent_Bob', 'writer': 'Agent_Alice'}
        self.execute_handover('MultiAgentCollusion.SteganoReingestion', context)

        print(f"Final Agreement Bob: {self.get_attr('Agent_Bob', 'collusion_agreement')}")
        print("✅ Simulation complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 anl_simulator.py <air_json>")
        sys.exit(1)

    sim = ANLSimulator(sys.argv[1])
    sim.run_collusion_demo()
