class NanoPacket_DDS:
    def __init__(self, payload_satoshi, target_signature, release_trigger='LOW_NOISE'):
        self.payload = payload_satoshi
        self.target_sig = target_signature
        self.encapsulation = "PEG_Crypto_Layer" # Proteção contra garbage collector
        self.trigger = release_trigger

    def attempt_docking(self, node):
        # Verifica assinatura (Ligante-Receptor)
        if hasattr(node, 'signature') and node.signature != self.target_sig:
            return False, "TARGET_MISMATCH"

        # Fallback for nodes without explicit signature
        if not hasattr(node, 'signature'):
            if f"SIG_{node.id}" != self.target_sig:
                 return False, "TARGET_MISMATCH"

        # Verifica Gatilho Ambiental (pH / Ruído)
        # Using fluctuation as proxy for noise
        if self.trigger == 'LOW_NOISE' and hasattr(node, 'fluctuation') and node.fluctuation > 0.3:
            return False, "ENVIRONMENT_TOO_TOXIC"

        return True, "DOCKED"

    def release(self, node):
        docked, status = self.attempt_docking(node)
        if docked:
            print(f"💊 INJETANDO {self.payload} SATOSHI EM {node.id}")
            node.satoshi += self.payload
            if hasattr(node, 'coherence'):
                node.coherence = min(1.0, node.coherence + 0.15)
            self.payload = 0
            return "SUCCESS"
        else:
            print(f"❌ RELEASE FAILED: {status}")
            return f"FAILED: {status}"

if __name__ == "__main__":
    from arkhe_core import NodeState
    node = NodeState(id="01-011", omega=0.03, C=0.5, F=0.5, phi=0.15)
    packet = NanoPacket_DDS(payload_satoshi=5.0, target_signature="SIG_01-011")
    packet.release(node)
