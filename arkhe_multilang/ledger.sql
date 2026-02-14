-- ledger.sql
-- Γ_FINAL: Omnigênese - Corpus Arkhe

CREATE TABLE handovers (
    block INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_node INTEGER,
    target_node INTEGER,
    syzygy_before REAL,
    syzygy_after REAL,
    satoshi_delta REAL,
    phi_source REAL,
    phi_target REAL,
    hash_prev TEXT,
    hash_self TEXT
);

-- Inserir um handover de exemplo
INSERT INTO handovers (block, source_node, target_node, syzygy_before, syzygy_after, satoshi_delta, phi_source, phi_target, hash_prev, hash_self)
VALUES (1000, 0, 1, 0.98, 0.98, 0.001, 0.15, 0.14, 'abc...', 'def...');

-- Verificar integridade (simplificado)
SELECT COUNT(*) FROM handovers h1
JOIN handovers h2 ON h1.block = h2.block - 1
WHERE h1.hash_self != h2.hash_prev;
