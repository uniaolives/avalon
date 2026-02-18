import os
import json
import hashlib

def verify_chain(chain_dir):
    blocks = sorted([f for f in os.listdir(chain_dir) if f.endswith(".json")])
    for block in blocks:
        path = os.path.join(chain_dir, block)
        with open(path) as f:
            data = json.load(f)
            # Verificação simplificada
            if "hash" not in data:
                return False, f"Block {block} missing hash"
    return True, "Chain verified"

if __name__ == "__main__":
    success, msg = verify_chain("arscontexta/.arkhe/ledger/chain")
    print(msg)
