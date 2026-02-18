# test_primordial_training.py
import numpy as np
from papercoder_kernel.core.primordial_glp import PrimordialGLP

def test_primordial_glp():
    print("🔥 Iniciando Teste de Treinamento Primordial...")

    # 1. Setup da rede
    input_dim = 16
    hidden1 = 32
    hidden2 = 16
    output = 4
    net = PrimordialGLP(input_dim, hidden1, hidden2, output)

    # 2. Gerar dados sintéticos (ex: 32 amostras)
    X = np.random.randn(32, input_dim)
    # Categorias aleatórias
    y = np.random.randint(0, output, 32)

    # 3. Loop de treinamento manual
    epochs = 100
    lr = 0.01

    print(f"▸ Treinando por {epochs} épocas (sem frameworks)...")
    initial_loss = net.loss(net.forward(X), y)
    print(f"   Loss Inicial: {initial_loss:.6f}")

    for epoch in range(epochs):
        net.forward(X)
        grad_norm = net.backward(X, y, lr=lr)

        if epoch % 10 == 0:
            current_loss = net.loss(net.y_pred, y)
            # print(f"   Época {epoch}: Loss = {current_loss:.6f}, Grad Norm = {grad_norm:.4f}")

    final_loss = net.loss(net.forward(X), y)
    print(f"   Loss Final: {final_loss:.6f}")

    assert final_loss < initial_loss, "A rede deve aprender e diminuir a loss"
    print("✅ Treinamento primordial validado.")

if __name__ == "__main__":
    test_primordial_glp()
