#!/bin/bash
# setup_merkabah7_federation.sh
# Adapted for simulation environment

echo "=============================================="
echo "MERKABAH-7: FEDERAÇÃO SOBRE DOUBLEZERO (MOCK)"
echo "Camada de transporte para handovers quânticos"
echo "=============================================="

# 1. MOCK INSTALLATION
echo "[1/5] Simulando instalação DoubleZero..."
chmod +x doublezero_mock.py
ln -sf $(pwd)/doublezero_mock.py ./doublezero
export PATH=$PATH:$(pwd)

echo "✓ DoubleZero 0.8.6-1 (MOCK) configurado"

# 2. FIREWALL (Skip in simulation)
echo "[2/5] Ignorando configuração de firewall em ambiente de simulação..."

# 3. IDENTITY
echo "[3/5] Gerando identidade DoubleZero/MERKABAH-7..."
./doublezero keygen
DZ_ID=$(./doublezero address)
echo "✓ DoubleZero ID: $DZ_ID"

# 4. CONNECTIVITY
echo "[4/5] Verificando malha de switches DoubleZero..."
./doublezero latency
echo "✓ Switches simulados alcançáveis"

# 5. METRICS (Skip systemd override)
echo "[5/5] Simulando exportação de métricas..."
echo "✓ Métricas ativas em localhost:2113 (SIMULATED)"

echo ""
echo "=============================================="
echo "SETUP SIMULADO CONCLUÍDO"
echo "=============================================="
echo "DoubleZero ID: $DZ_ID"
echo "Status: $(./doublezero status)"
echo ""
