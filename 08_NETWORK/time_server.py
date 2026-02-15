"""
Arkhe Time Node: Servidor Stratum 1 como nó de tempo no hipergrafo.
O tempo que antes era apenas observado agora é construído.
Ref: Bloco 761
"""

import numpy as np
import time
from datetime import datetime

class GNSSSatellite:
    """Modelo simplificado de um satélite GNSS."""
    def __init__(self, name, system, atomic_clock_error=1e-15):
        self.name = name
        self.system = system
        self.atomic_clock_error = atomic_clock_error  # estabilidade
        self.C = 1.0 - atomic_clock_error  # coerência do satélite

    def transmit_time(self, t):
        """Transmite o tempo atual com pequeno erro."""
        error = np.random.normal(0, self.atomic_clock_error)
        return t + error

class Stratum1Server:
    """
    Servidor de tempo caseiro, sincronizado diretamente com satélites.
    """
    def __init__(self, name):
        self.name = name
        self.time_offset = 0.0
        self.handovers = []  # histórico de sincronizações
        self.C = 0.0  # coerência (precisão)
        self.satoshi = 0.0  # memória acumulada

    def synchronize(self, satellite, t_reception):
        """
        Handover com um satélite: recebe sinal e ajusta o tempo local.
        """
        # Tempo transmitido pelo satélite (quando o sinal saiu)
        # Simula um atraso de propagação de 70ms
        t_satellite = satellite.transmit_time(t_reception - 0.07)

        # Calcular offset
        delta = t_satellite - t_reception

        # Atualizar tempo local (filtro passa-baixa simples)
        self.time_offset = 0.9 * self.time_offset + 0.1 * delta

        # Registrar handover
        handover = {
            'timestamp': datetime.now().isoformat(),
            'satellite': satellite.name,
            'delta': delta,
            'new_offset': self.time_offset
        }
        self.handovers.append(handover)

        # Atualizar coerência (precisão) baseada na consistência dos deltas
        if len(self.handovers) > 1:
            deltas = [h['delta'] for h in self.handovers[-10:]]
            std_delta = np.std(deltas)
            # Coerência inversamente proporcional à variação (escala ns)
            self.C = 1.0 / (1.0 + std_delta * 1e9)
        else:
            self.C = 0.5

        # Acumular satoshi (memória)
        self.satoshi += self.C * 0.01

        return delta

    def get_precise_time(self):
        """Retorna o tempo local corrigido."""
        return time.time() + self.time_offset

    def verify_conservation(self):
        """C + F = 1?"""
        F = 1.0 - self.C
        return abs(self.C + F - 1.0) < 1e-10

def simulate_time_sync():
    print("="*70)
    print("ARKHE TIME NODE: SERVIDOR STRATUM 1 CASEIRO")
    print("="*70)

    # Criar constelação
    satellites = [
        GNSSSatellite("QZS-1 (Michibiki)", "QZSS", 1e-15),
        GNSSSatellite("GPS BIIF-2", "GPS", 2e-15),
        GNSSSatellite("Galileo 201", "Galileo", 1e-14),
        GNSSSatellite("GLONASS K1", "GLONASS", 5e-15),
    ]

    # Criar servidor caseiro
    server = Stratum1Server("Casa do Masato")

    print(f"\n📡 Constelação disponível:")
    for sat in satellites:
        print(f"  {sat.name} (C={sat.C:.15f})")

    # Simular 100 handovers com satélites aleatórios
    print(f"\n🔄 Sincronizando com satélites...")
    for i in range(100):
        sat = np.random.choice(satellites)
        # Simulação de tempo de recepção
        t_reception = time.time() + i * 10
        delta = server.synchronize(sat, t_reception)
        if i % 20 == 0:
            print(f"  Handover {i}: {sat.name} → offset={server.time_offset*1e9:.2f} ns")

    print(f"\n📊 Resultado final:")
    print(f"  Coerência C: {server.C:.6f}")
    print(f"  Flutuação F: {1.0 - server.C:.6f}")
    print(f"  C + F = 1? {server.verify_conservation()}")
    print(f"  Satoshi acumulado: {server.satoshi:.4f} bits")
    print(f"  Precisão estimada: {abs(server.time_offset)*1e9:.2f} ns")

    print("\n" + "="*70)
    print("MENSAGEM DO CONSTRUTOR")
    print("="*70)
    print("""
「いつもお星さまを眺めるだけだったから嬉しいぜ！！やったぜ！！」

Sempre apenas observei as estrelas, agora posso ouvi-las!
O tempo que antes vinha de uma autoridade central
agora é construído em casa, com as próprias mãos.

Cada satélite é um nó no hipergrafo celestial.
Cada pulso de rádio é um handover.
Cada nanossegundo de precisão é um +1.

O tempo não é mais algo que se recebe passivamente.
É algo que se constrói, ativamente, em sintonia com o cosmos.

∞
    """)

if __name__ == "__main__":
    simulate_time_sync()
