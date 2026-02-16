# arkhenet/config.py
"""
Configurações da simulação ArkheNet.
"""

SIM_TIME = 1000          # tempo total de simulação (horas simuladas)
INITIAL_FUNDS = 100.0    # saldo inicial de cada autômato (USDC)
COMPUTE_COST_PER_HOUR = 0.05  # custo de computação por hora
INFERENCE_COST = 0.02    # custo por chamada de inferência
RADIO_BANDWIDTH = 10     # capacidade do canal (mensagens por hora)
SPAWN_THRESHOLD = 50.0   # saldo mínimo para reprodução
SPAWN_COST = 20.0        # custo para criar um filho
LEARNING_RATE = 0.1      # taxa de evolução
MAX_NODES = 100          # número máximo de autômatos
