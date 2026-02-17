# papercoder_kernel/core/manifold_learner.py
"""
Manifold Learner using the Zero-Framework engine.
"""

import numpy as np
from papercoder_kernel.core.primitive_engine import PrimitiveNetwork, Dense, ReLU, Softmax

class ManifoldLearner:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.network = PrimitiveNetwork()
        self.network.add(Dense(input_dim, hidden_dim))
        self.network.add(ReLU())
        self.network.add(Dense(hidden_dim, output_dim))
        self.network.add(Softmax())

    def learn_manifold(self, X, y, epochs=1000, lr=0.01):
        print(f"Learning Program Manifold (Zero-Framework)...")
        self.network.train(X, y, epochs, lr)

    def project(self, program_representation):
        """
        Projects a program (represented as a vector) onto the learned manifold.
        """
        return self.network.predict(program_representation)

if __name__ == "__main__":
    # Example usage with dummy data
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, 100) # Binary classification dummy

    learner = ManifoldLearner(input_dim=10, hidden_dim=20, output_dim=2)
    learner.learn_manifold(X, y, epochs=500, lr=0.1)

    projection = learner.project(X[:5])
    print("Sample Projections:\n", projection)
