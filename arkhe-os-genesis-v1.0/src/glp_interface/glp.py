from flask import Flask, request, jsonify
import torch
import numpy as np

app = Flask(__name__)

# Carrega modelo GLP (simplificado)
class GLPServer:
    def __init__(self):
        self.meta_neurons = 128
        # Simula pesos
        self.weights = torch.randn(self.meta_neurons, 64)

    def encode(self, activation):
        # Projeção em meta‑neurônios
        return torch.matmul(activation, self.weights.T).tolist()

glp = GLPServer()

@app.route('/encode', methods=['POST'])
def encode():
    data = request.json
    activation = torch.tensor(data['activation'])
    meta = glp.encode(activation)
    return jsonify({'meta': meta})

@app.route('/steer', methods=['POST'])
def steer():
    data = request.json
    # Aplica direção de conceito
    meta = np.array(data['meta'])
    direction = np.array(data['direction'])
    strength = data.get('strength', 1.0)
    steered = meta + strength * direction
    return jsonify({'steered': steered.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
