# papercoder_kernel/core/primitive_engine.py
"""
Zero-Framework Neural Engine (Γ_atom).
"Forget frameworks. Learn the math."
"""

import numpy as np

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        raise NotImplementedError

    def backward(self, output_gradient, learning_rate):
        raise NotImplementedError

class Dense(Layer):
    def __init__(self, input_size, output_size):
        # He Initialization for weights
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.bias = np.zeros((1, output_size))

    def forward(self, input):
        self.input = input
        # y = xW + b
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, output_gradient, learning_rate):
        # dL/dW = x^T * dL/dy
        weights_gradient = np.dot(self.input.T, output_gradient)
        # dL/dB = Σ dL/dy
        bias_gradient = np.sum(output_gradient, axis=0, keepdims=True)
        # dL/dx = dL/dy * W^T
        input_gradient = np.dot(output_gradient, self.weights.T)

        # Update parameters
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * bias_gradient

        return input_gradient

class ReLU(Layer):
    def forward(self, input):
        self.input = input
        return np.maximum(0, input)

    def backward(self, output_gradient, learning_rate):
        # derivative of ReLU is 1 if x > 0 else 0
        return output_gradient * (self.input > 0)

class Softmax(Layer):
    def forward(self, input):
        # Numerically stable softmax
        exp_values = np.exp(input - np.max(input, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        return self.output

    def backward(self, output_gradient, learning_rate):
        # Note: Softmax is usually handled together with CrossEntropy for efficiency.
        # This is a general implementation.
        n = np.size(self.output)
        return np.dot(output_gradient, (np.identity(n) - self.output.T) * self.output)

def cross_entropy_loss(y_true, y_pred):
    """
    Categorical Cross Entropy Loss.
    """
    samples = len(y_pred)
    y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

    if len(y_true.shape) == 1: # Categorical labels
        correct_confidences = y_pred_clipped[range(samples), y_true]
    elif len(y_true.shape) == 2: # One-hot encoded
        correct_confidences = np.sum(y_pred_clipped * y_true, axis=1)

    return -np.log(correct_confidences)

def cross_entropy_softmax_backward(y_true, y_pred):
    """
    Combined derivative of Softmax and CrossEntropy.
    dL/dz = y_pred - y_true
    """
    samples = len(y_pred)
    if len(y_true.shape) == 1:
        y_true = np.eye(y_pred.shape[1])[y_true]

    return (y_pred - y_true) / samples

class PrimitiveNetwork:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_derivative = None

    def add(self, layer):
        self.layers.append(layer)

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            # Forward pass
            output = X
            for layer in self.layers:
                output = layer.forward(output)

            # Compute loss (assuming last layer is softmax + CE)
            loss = np.mean(cross_entropy_loss(y, output))

            # Backward pass
            gradient = cross_entropy_softmax_backward(y, output)
            for layer in reversed(self.layers[:-1]): # Skip the explicit Softmax layer if handled here
                 # Note: If we use the combined backward, we skip the last activation backward.
                 # This is a bit tricky depending on how layers are added.
                 # For simplicity, we assume the last layer in self.layers is Dense
                 # and we handle Softmax+CE externally.
                 pass

            # Let's refine the loop
            grad = cross_entropy_softmax_backward(y, output)
            for layer in reversed(self.layers):
                if isinstance(layer, Softmax):
                    continue # handled by combined backward
                grad = layer.backward(grad, learning_rate)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss:.6f}")

    def predict(self, X):
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output
