from anl import *
import numpy as np

def test_active_inference_belief_update():
    print("Testing Active Inference Belief Update...")
    n_states = 10
    n_obs = 10
    space = StateSpace(n_states, "euclidean", "real")

    agent = ActiveInferenceNode("AGI", space, n_states, n_obs)

    # Target observation: index 0
    obs_idx = 0

    # Likelihood matrix A is initially flat (plus some noise/epsilon)
    # So initial belief is flat.
    initial_belief = agent.state.copy()

    # We perform an update given observation 0
    agent.update_belief(obs_idx)
    final_belief = agent.state

    print(f"Initial belief[0]: {initial_belief[0]:.4f}")
    print(f"Final belief[0]: {final_belief[0]:.4f}")

    # In a flat likelihood, belief[0] might not change much unless A is biased.
    # Dirichlet is initialized with 0.1, so it's flat.
    # likelihood = A[0, :] = 0.1 / (0.1 * 10) = 0.1.
    # posterior = 0.1 * 0.1 = 0.01. Sum = 0.1. Normalised = 0.1.
    # So it stays flat.

    # Let's bias the likelihood and try again.
    agent.a_dirichlet[0, 0] = 5.0 # Observation 0 is very likely in state 0

    agent.update_belief(obs_idx)
    final_belief = agent.state

    print(f"After bias, belief[0]: {final_belief[0]:.4f}")
    assert final_belief[0] > initial_belief[0]
    print("✅ Active Inference belief update verified.")

def test_active_inference_learning():
    print("Testing Active Inference Dirichlet Learning...")
    n_states = 2
    n_obs = 2
    space = StateSpace(n_states, "euclidean", "real")

    agent = ActiveInferenceNode("Learner", space, n_states, n_obs)

    # Initial A
    A_initial = agent.get_A().copy()

    # Observe 0 while in state 0 (set belief to state 0)
    agent.state = np.array([1.0, 0.0])
    agent.learn(0)

    A_final = agent.get_A()
    print(f"Initial A[0,0]: {A_initial[0,0]:.4f}")
    print(f"Final A[0,0]: {A_final[0,0]:.4f}")

    assert A_final[0,0] > A_initial[0,0]
    print("✅ Active Inference learning verified.")

if __name__ == "__main__":
    test_active_inference_belief_update()
    test_active_inference_learning()
