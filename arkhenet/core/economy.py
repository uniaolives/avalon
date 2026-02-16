# arkhenet/core/economy.py
class x402:
    """Protocolo de pagamento simples."""
    @staticmethod
    def pay(sender, receiver, amount):
        if sender.wallet >= amount:
            sender.wallet -= amount
            receiver.wallet += amount
            return True
        return False
