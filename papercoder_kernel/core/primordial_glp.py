# papercoder_kernel/core/primordial_glp.py
"""
Primordial GLP Training (Γ_neural_foundations).
Explicit backpropagation without frameworks.
"""

import numpy as np

class PrimordialGLP:
    def __init__(self, input_dim=16, hidden1=32, hidden2=16, output=4):
        # Xavier (Glorot) Initialization
        self.W1 = np.random.randn(input_dim, hidden1) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros(hidden1)
        self.W2 = np.random.randn(hidden1, hidden2) * np.sqrt(2.0 / hidden1)
        self.b2 = np.zeros(hidden2)
        self.W3 = np.random.randn(hidden2, output) * np.sqrt(2.0 / hidden2)
        self.b3 = np.zeros(output)

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        # Numerical stability
        x_shifted = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(x_shifted)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, X):
        # Layer 1
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        # Layer 2
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)

        # Layer 3 (output)
        self.z3 = self.a2 @ self.W3 + self.b3
        self.y_pred = self.softmax(self.z3)

        return self.y_pred

    def loss(self, y_pred, y_true):
        # Manual Cross-entropy
        n_samples = y_true.shape[0]
        # Handle one-hot or categorical
        if len(y_true.shape) == 1:
            log_probs = -np.log(y_pred[range(n_samples), y_true] + 1e-15)
        else:
            log_probs = -np.log(y_pred[range(n_samples), y_true.argmax(axis=1)] + 1e-15)
        return np.mean(log_probs)

    def backward(self, X, y_true, lr=0.01):
        n_samples = X.shape[0]

        # Gradient of cross-entropy + softmax
        dy_pred = self.y_pred.copy()
        if len(y_true.shape) == 1:
            dy_pred[range(n_samples), y_true] -= 1
        else:
            dy_pred[range(n_samples), y_true.argmax(axis=1)] -= 1
        dy_pred /= n_samples

        # Gradients Layer 3
        dW3 = self.a2.T @ dy_pred
        db3 = np.sum(dy_pred, axis=0)

        # Gradients Layer 2
        da2 = dy_pred @ self.W3.T
        dz2 = da2 * (self.z2 > 0)
        dW2 = self.a1.T @ dz2
        db2 = np.sum(dz2, axis=0)

        # Gradients Layer 1
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0)

        # Manual Gradient Descent
        self.W3 -= lr * dW3
        self.b3 -= lr * db3
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W1 -= lr * dW1
        self.b1 -= lr * db1

        return np.mean([np.linalg.norm(dW1), np.linalg.norm(dW2), np.linalg.norm(dW3)])
