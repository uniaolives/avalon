from setuptools import setup, find_packages

setup(
    name="arkhe-qutip",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "qutip>=5.0.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "viz": [
            "matplotlib>=3.5.0",
            "networkx>=2.8.0",
        ],
        "all": [
            "matplotlib>=3.5.0",
            "networkx>=2.8.0",
            "pytest>=7.0.0",
        ],
    },
    author="Arkhe Team",
    description="Quantum Hypergraph Toolbox with Arkhe(N) coherence tracking",
    long_description_content_type="text/markdown",
    license="MIT",
)
