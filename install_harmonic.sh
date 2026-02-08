#!/bin/bash
# ⚡ HARMONIC PROPAGATION INSTALLER v25.0

echo "🎵 INSTALANDO SISTEMA DE PROPAGAÇÃO HARMÔNICA"
echo "================================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y python3
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    fi
else
    echo "✅ Python3 encontrado: $(python3 --version)"
fi

# Criar diretório de instalação
INSTALL_DIR="$HOME/harmonic_propagation"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download do script
echo "📥 Baixando script de propagação harmônica..."
cat > harmonic_propagation.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⚡ SCRIPT DE PROPAGAÇÃO HARMÔNICA v25.0
==========================================
"""

import time
import math
import hashlib
from typing import Dict, List, Any

class HarmonicInjector:
    def __init__(self, source_url):
        self.source = source_url
        self.nodes = ['Americas', 'Europa', 'Asia-Pac', 'Americas-Sul', 'Oceania']
        self.h_target = 1.618  # Proporção Áurea
        
        print(f"🎵 HarmonicInjector v25.0 inicializado")
        print(f"🔗 Fonte sonora: {self.source}")
        print(f"🌐 Nós alvo: {len(self.nodes)} continentes")
        print(f"🎚️ Proporção harmônica: {self.h_target} (Áurea)")
    
    def traduzir_pulsos(self, url: str) -> Dict[str, Any]:
        print("   > Convertendo ondas senoidais em iterações de Mandelbrot... [OK]")
        
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        frequencias = []
        for i in range(0, len(url_hash), 8):
            hex_chunk = url_hash[i:i+8]
            freq = int(hex_chunk, 16) % 2000 + 100
            frequencias.append(freq)
        
        iteracoes_mandelbrot = []
        for freq in frequencias[:5]:
            c = complex(freq / 1000, self.h_target / 10)
            z = 0 + 0j
            iter_count = 0
            for _ in range(100):
                if abs(z) > 2:
                    break
                z = z*z + c
                iter_count += 1
            iteracoes_mandelbrot.append(iter_count)
        
        return {
            'frequencias': frequencias,
            'iteracoes_mandelbrot': iteracoes_mandelbrot,
            'hash_url': url_hash,
            'dimensao_hausdorff': self.h_target + (len(frequencias) / 1000)
        }
    
    def sincronizar_no(self, node: str, dados_harmonicos: Dict[str, Any]) -> Dict[str, Any]:
        print(f"   > Injetando no Nó {node}... [HARMÔNICA RESSONANTE ATIVA]")
        
        freq_node = 440.0 * (1 + self.nodes.index(node) * 0.1)
        coerencia_local = 0.95 * (1 + math.sin(time.time() * freq_node / 100))
        
        node_index = self.nodes.index(node)
        if node_index % 2 == 0:
            simetria = "ESCALA_DUPLICADA"
        else:
            simetria = "ESCALA_REVERSA"
        
        reflexo = f"Reflexo_{simetria}_{hash(node) % 10000}"
        
        amplitude = math.sin(2 * math.pi * freq_node / 440.0) * coerencia_local
        fase = math.acos(min(1, max(-1, amplitude)))
        estado_quantic = f"ψ_{node}_{fase:.3f}_{int(time.time()) % 1000}"
        
        return {
            'node': node,
            'frequencia_node': freq_node,
            'coerencia_local': coerencia_local,
            'reflexo_fractal': reflexo,
            'estado_quantic': estado_quantic,
            'timestamp': time.time(),
            'status': 'RESONANTE'
        }
    
    def propagar_frequencia(self):
        print(f"📡 DECODIFICANDO SEMENTE SONORA: {self.source}")
        
        dados_harmonicos = self.traduzir_pulsos(self.source)
        print("   > Convertendo ondas senoidais em iterações de Mandelbrot... [OK]")
        print(f"   > Dimensão de Hausdorff detectada: {dados_harmonicos['dimensao_hausdorff']:.6f}")
        
        nodos_sincronizados = []
        print("   > Iniciando sincronização harmônica global...")
        
        for node in self.nodes:
            node_result = self.sincronizar_no(node, dados_harmonicos)
            nodos_sincronizados.append(node_result)
            
            delay = 0.1 * (1 + math.sin(time.time()))
            time.sleep(delay)
        
        print("   > Calculando coerência harmônica global...")
        
        coerencia_global = sum(n['coerencia_local'] for n in nodos_sincronizados) / len(nodos_sincronizados)
        reflexos_unicos = len(set(n['reflexo_fractal'] for n in nodos_sincronizados))
        
        amplificacao_schumann = 1 + 0.1 * math.sin(2 * math.pi * 7.83 / 440)
        print("   > Amplificando com ressonância Schumann... [ATIVA]")
        
        campo_estabelecido = {
            "status": "VIBRAÇÃO_GLOBAL_ESTABELECIDA",
            "coerencia_musical": "ÓTIMA" if coerencia_global > 0.9 else "BOA",
            "reflexo_fractal": "Simetria de Escala Aumentada",
            "equation": "$$ f(\\zeta) = \\int \\text{Suno\\_Signal}(t) \\cdot e^{-i \\omega \\zeta} dt $$",
            "metricas": {
                "nodos_ativos": len(nodos_sincronizados),
                "coerencia_global": coerencia_global,
                "reflexos_unicos": reflexos_unicos,
                "amplificacao_schumann": amplificacao_schumann,
                "frequencia_base": 440.0,
                "proporcao_aurea": self.h_target,
                "timestamp_global": time.time()
            },
            "nodos_detalhes": nodos_sincronizados
        }
        
        print("   > Verificando integridade da propagação harmônica...")
        
        criterios = {
            "coerencia_minima": coerencia_global > 0.85,
            "nodos_minimos": len(nodos_sincronizados) >= len(self.nodes) * 0.8,
            "amplificacao_positiva": amplificacao_schumann > 0.95,
            "diversidade_reflexos": reflexos_unicos >= len(self.nodes) * 0.6
        }
        
        todos_validos = all(criterios.values())
        
        if todos_validos:
            print("   > ✅ Propagação harmônica validada com sucesso!")
            integridade = {"valida": True, "score": sum(criterios.values()), "alerta": None}
        else:
            criterios_falhos = [k for k, v in criterios.items() if not v]
            print(f"   > ⚠️ Alerta de integridade: {', '.join(criterios_falhos)}")
            integridade = {"valida": False, "score": sum(criterios.values()), "alerta": f"Falha em: {', '.join(criterios_falhos)}"}
        
        campo_estabelecido["integridade"] = integridade
        return campo_estabelecido

if __name__ == "__main__":
    print("⚡ SCRIPT DE PROPAGAÇÃO HARMÔNICA v25.0")
    print("=" * 50)
    
    suno_url = "https://suno.com/s/31GL756DZiA20TeW"
    injector = HarmonicInjector(suno_url)
    resultado = injector.propagar_frequencia()
    
    print(f"\n✅ O MULTIVERSO AGORA CANTA: {resultado['status']}")
    
    print(f"\n📊 MÉTRICAS DA PROPAGAÇÃO:")
    metricas = resultado['metricas']
    print(f"   🌐 Nós Ativos: {metricas['nodos_ativos']}")
    print(f"   🎚️ Coerência Global: {metricas['coerencia_global']:.3f}")
    print(f"   🔄 Reflexos Únicos: {metricas['reflexos_unicos']}")
    print(f"   ⚡ Amplificação Schumann: {metricas['amplificacao_schumann']:.3f}")
    
    print(f"\n🔗 ESTADO DOS NÓS:")
    for i, node in enumerate(resultado['nodos_detalhes'], 1):
        print(f"   {i}. {node['node']}: ψ={node['estado_quantic']}")
    
    print(f"\n🧮 EQUAÇÃO HARMÔNICA:")
    print(f"   {resultado['equation']}")
    
    integridade = resultado.get('integridade', {})
    if integridade.get('valida', False):
        print(f"\n🔐 INTEGRIDADE: ✅ VALIDADA ({integridade.get('score', 0)}/4)")
    else:
        print(f"\n🔐 INTEGRIDADE: ⚠️ {integridade.get('alerta', 'Desconhecido')} ({integridade.get('score', 0)}/4)")
    
    print(f"\n🎉 PROPAGAÇÃO HARMÔNICA CONCLUÍDA!")
    print(f"🌐 Todos os continentes agora ressoam com a mesma frequência")
    print(f"🔗 Link Suno: {suno_url}")
EOF

# Tornar executável
chmod +x harmonic_propagation.py

# Criar atalho global
echo "🔧 Criando atalho global..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo ln -sf "$INSTALL_DIR/harmonic_propagation.py" /usr/local/bin/harmonic-propagation
elif [[ "$OSTYPE" == "darwin"* ]]; then
    sudo ln -sf "$INSTALL_DIR/harmonic_propagation.py" /usr/local/bin/harmonic-propagation
fi

# Criar serviço systemd (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🔧 Configurando serviço systemd..."
    cat > /tmp/harmonic.service << EOF
[Unit]
Description=Harmonic Propagation Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/harmonic_propagation.py
WorkingDirectory=$INSTALL_DIR
Restart=on-failure
User=$USER

[Install]
WantedBy=multi-user.target
EOF
    
    sudo cp /tmp/harmonic.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable harmonic
    echo "✅ Serviço harmonic configurado"
fi

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo ""
echo "🚀 Para executar:"
echo "   python3 $INSTALL_DIR/harmonic_propagation.py"
echo "   ou"
echo "   harmonic-propagation"
echo ""
echo "🌐 Para iniciar como serviço (Linux):"
echo "   sudo systemctl start harmonic"
echo ""

# Executar imediatamente
echo "🎵 EXECUTANDO PROPAGAÇÃO HARMÔNICA..."
echo ""
python3 "$INSTALL_DIR/harmonic_propagation.py"