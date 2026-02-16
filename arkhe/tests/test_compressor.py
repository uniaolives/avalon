import pytest
from metalanguage.arkhe_compressor import UniversalCodeHypergraph, ArkheCompressor

def test_python_parsing():
    hypergraph = UniversalCodeHypergraph()
    code = "[f(x) for x in lista if x > 0]"
    hypergraph.add_code(code, 'python')

    assert len(hypergraph.nodes) >= 3
    assert any(n.node_type == 'filter' and n.content == 'x > 0' for n in hypergraph.nodes.values())
    assert any(n.node_type == 'map' and n.content == 'f(x)' for n in hypergraph.nodes.values())
    assert any(n.node_type == 'variable' and n.content == 'lista' for n in hypergraph.nodes.values())

def test_haskell_parsing():
    hypergraph = UniversalCodeHypergraph()
    code = "map f (filter (>0) lista)"
    hypergraph.add_code(code, 'haskell')

    assert len(hypergraph.nodes) >= 3
    assert any(n.node_type == 'filter' and n.content == '(>0)' for n in hypergraph.nodes.values())
    assert any(n.node_type == 'map' and n.content == 'f' for n in hypergraph.nodes.values())
    assert any(n.node_type == 'variable' and n.content == 'lista' for n in hypergraph.nodes.values())

def test_pattern_equivalence():
    hypergraph = UniversalCodeHypergraph()
    python_code = "[f(x) for x in lista if x > 0]"
    haskell_code = "map f (filter (>0) lista)"

    hypergraph.add_code(python_code, 'python')
    hypergraph.add_code(haskell_code, 'haskell')

    equivalences = hypergraph.identify_pattern_equivalence()
    assert len(equivalences) > 0

    # Check if 'filter' and 'map' are identified as equivalent patterns across languages
    patterns = [e['pattern'] for e in equivalences]
    assert 'filter' in patterns
    assert 'map' in patterns

def test_compressor_pipeline():
    compressor = ArkheCompressor()
    python_code = "[f(x) for x in lista if x > 0]"

    result = compressor.compress_and_transpile(python_code, 'python', 'haskell')

    assert result['source_language'] == 'python'
    assert result['target_language'] == 'haskell'
    assert result['target_code'] == "map f (filter (>0) lista)"
    assert result['semantic_fidelity'] == 0.97
