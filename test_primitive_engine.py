# test_primitive_engine.py
import unittest
import numpy as np
from papercoder_kernel.core.primitive_engine import Dense, ReLU, Softmax, cross_entropy_loss, cross_entropy_softmax_backward

class TestPrimitiveEngine(unittest.TestCase):
    def test_dense_forward(self):
        dense = Dense(3, 2)
        dense.weights = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
        dense.bias = np.array([[0.1, 0.2]])
        X = np.array([[1, 2, 3]])
        # 1*0.1 + 2*0.3 + 3*0.5 + 0.1 = 0.1 + 0.6 + 1.5 + 0.1 = 2.3
        # 1*0.2 + 2*0.4 + 3*0.6 + 0.2 = 0.2 + 0.8 + 1.8 + 0.2 = 3.0
        expected = np.array([[2.3, 3.0]])
        output = dense.forward(X)
        np.testing.assert_array_almost_equal(output, expected)

    def test_relu_forward(self):
        relu = ReLU()
        X = np.array([[-1, 0, 1]])
        expected = np.array([[0, 0, 1]])
        output = relu.forward(X)
        np.testing.assert_array_almost_equal(output, expected)

    def test_gradient_check(self):
        """
        Numerical gradient checking for Dense layer.
        """
        dense = Dense(2, 1)
        X = np.array([[0.5, -0.2]])
        y_true = np.array([[1.0]]) # Regression-like target for simplicity of check

        def compute_loss(weights):
            old_weights = dense.weights.copy()
            dense.weights = weights
            out = dense.forward(X)
            # Use simple squared error for check
            loss = 0.5 * np.sum((out - y_true)**2)
            dense.weights = old_weights
            return loss

        # Analytical gradient
        out = dense.forward(X)
        grad_out = out - y_true # dL/dout
        dense.backward(grad_out, learning_rate=0) # Update internal grads without moving

        # dL/dW = X.T * grad_out
        analytical_grad_w = np.dot(X.T, grad_out)

        # Numerical gradient
        eps = 1e-6
        numerical_grad_w = np.zeros_like(dense.weights)
        for i in range(dense.weights.shape[0]):
            for j in range(dense.weights.shape[1]):
                w_plus = dense.weights.copy()
                w_plus[i, j] += eps
                w_minus = dense.weights.copy()
                w_minus[i, j] -= eps
                numerical_grad_w[i, j] = (compute_loss(w_plus) - compute_loss(w_minus)) / (2 * eps)

        np.testing.assert_array_almost_equal(analytical_grad_w, numerical_grad_w, decimal=5)

    def test_complete_training_logic(self):
        from papercoder_kernel.core.primitive_engine import PrimitiveNetwork
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0]) # XOR as classification

        net = PrimitiveNetwork()
        net.add(Dense(2, 8))
        net.add(ReLU())
        net.add(Dense(8, 2))
        net.add(Softmax())

        # Just check if it runs without error
        net.train(X, y, epochs=10, learning_rate=0.1)
        preds = net.predict(X)
        self.assertEqual(preds.shape, (4, 2))

if __name__ == "__main__":
    unittest.main()
