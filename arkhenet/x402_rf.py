# x402_rf.py
import socket
import time
import hashlib

class RFTransceiver:
    def __init__(self, interface: str, frequency: float):
        self.interface = interface
        self.frequency = frequency
        # Simula criação de socket para rádio
        # self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

    def send_message(self, to_mac: bytes, payload: bytes, price: float) -> bool:
        """Envia mensagem via RF e debita o preço (simulação)"""
        # Simula envio
        message = to_mac + payload + str(price).encode()
        checksum = hashlib.sha256(message).digest()[:4]
        packet = message + checksum
        # Aqui iria para a camada de rádio
        print(f"Enviando {len(packet)} bytes para {to_mac.hex()[:8]}...")
        time.sleep(0.01)  # simula latência
        return True

    def receive_message(self) -> tuple:
        """Recebe pacote e retorna (from_mac, payload, price)"""
        # Simulação: aguarda 0.1s e retorna um pacote de teste
        time.sleep(0.1)
        return (b'\x01\x02\x03\x04\x05\x06', b'Hello', 0.01)
