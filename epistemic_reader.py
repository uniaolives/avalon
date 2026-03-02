import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from anl import ActiveInferenceNode, StateSpace

def simulate_epistemic_reader():
    print("Initializing Epistemic Document Reader Simulation...")

    # 1. Generate synthetic documents (to avoid download issues)
    topics = ['Space', 'Graphics', 'Baseball']
    n_topics = len(topics)
    n_docs = 30

    # Create vocabulary
    vocab = ['galaxy', 'star', 'rocket', 'orbit', 'pixel', 'render', 'shader', 'vector', 'homerun', 'strike', 'pitch', 'bat']
    topic_words = [
        ['galaxy', 'star', 'rocket', 'orbit'], # Space
        ['pixel', 'render', 'shader', 'vector'], # Graphics
        ['homerun', 'strike', 'pitch', 'bat']    # Baseball
    ]

    documents = []
    doc_labels = []
    for i in range(n_docs):
        topic_idx = i % n_topics
        doc_labels.append(topic_idx)
        # Generate document with words mostly from its topic
        words = np.random.choice(topic_words[topic_idx], 5).tolist()
        words += np.random.choice(vocab, 2).tolist() # Add some noise
        documents.append(" ".join(words))

    # Vectorize documents
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents).toarray()

    # 2. Setup Active Inference Agent
    # n_states = n_topics, n_obs = n_docs
    space = StateSpace(n_topics, "discrete", "real")
    agent = ActiveInferenceNode("ReaderAgent", space, n_topics, n_docs)

    # Simulate a transition matrix B (Simplified: reading a doc doesn't change underlying topic)
    B = np.zeros((n_topics, n_topics, n_docs))
    for a in range(n_docs):
        B[:, :, a] = np.eye(n_topics)

    print(f"Library loaded with {n_docs} documents across {n_topics} topics.")

    # 3. Reading Loop
    read_docs = set()
    history = []

    for step in range(15):
        # Calculate Expected Free Energy G for all possible documents (actions)
        # Note: In our current anl.py, compute_epistemic_G returns values to be MAXIMIZED (high epistemic value)
        # But compute_G returns values to be MINIMIZED.
        G = agent.compute_epistemic_G(B)

        # Penalize already read documents
        for doc_idx in read_docs:
            G[doc_idx] = -1e9

        # Choose document with highest Epistemic Value (Curiosity)
        best_doc_idx = np.argmax(G)

        if G[best_doc_idx] < 1e-4:
            print(f"Step {step}: Agent is BORED. All significant uncertainty reduced.")
            break

        # "Read" the document
        read_docs.add(best_doc_idx)

        # In this simulation, the "observation" is the document index itself,
        # and the outcome relates to the hidden state (topic).
        # Actually, ActiveInferenceNode.update_belief takes observation_idx.
        # But here, choosing a document is an ACTION. The observation should be the content.
        # Let's map topics to observation indices 0, 1, 2.
        obs_idx = doc_labels[best_doc_idx]

        # Update Belief and Learn
        agent.update_belief(obs_idx)
        agent.learn(obs_idx)

        history.append((best_doc_idx, G[best_doc_idx]))
        print(f"Step {step}: Reading Doc {best_doc_idx} (Topic: {topics[obs_idx]}). Epistemic Value: {G[best_doc_idx]:.4f}")

    print("Simulation Complete.")

if __name__ == "__main__":
    simulate_epistemic_reader()
