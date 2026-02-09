import requests
import numpy as np

# Gera 12800 pontos de dados simulando um hipercubo (10x10x8x16)
mock_data = np.random.rand(12800).tolist()

nodes = ["http://localhost:8000"] # Adjusted to a single node on port 8000

for node in nodes:
    print(f"--- Solicitando Scan no {node} ---")
    try:
        response = requests.post(f"{node}/qhttp/scan", json={
            "node_id": "MERKABAH_CMD_01",
            "spectral_data": mock_data,
            "metadata": {"target": "Exoplanet_Sector_G"}
        })
        print(response.json())
    except Exception as e:
        print(f"Erro ao conectar ao nó {node}: {e}")
