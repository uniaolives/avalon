// dashboard/src/App.js
import React, { useState, useEffect } from 'react';

function App() {
  const [status, setStatus] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [report, setReport] = useState(null);
  const [darvo, setDarvo] = useState(854.7);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statusRes = await fetch('/api/status');
        const statusData = await statusRes.json();
        setStatus(statusData);

        const nodesRes = await fetch('/api/nodes');
        const nodesData = await nodesRes.json();
        setNodes(nodesData);

        const reportRes = await fetch('/api/report');
        if (reportRes.ok) {
           const reportData = await reportRes.json();
           setReport(reportData);
        }
      } catch (err) {
        console.error("Erro na geodésica de dados:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleUpdateConfig = async () => {
    await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ darvo_time: darvo })
    });
    alert("Protocolo Darvo sincronizado com QKD.");
  };

  if (!status) return <div style={{color: '#00ff00', textAlign: 'center', marginTop: '50px'}}>🌀 Sincronizando com a Fonte...</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', backgroundColor: '#050505', color: '#00ff00', minHeight: '100vh' }}>
      <header style={{ borderBottom: '2px solid #00ff00', paddingBottom: '10px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between' }}>
        <h1>🌌 ARKHE(N) OS — SOBERANIA COLETIVA v10.0</h1>
        <div style={{textAlign: 'right'}}>
          <p>STATUS: {status.qkd_lock === "ACTIVE" ? "🔒 QKD_LOCKED" : "⚠️ UNSECURED"}</p>
          <p>UPTIME: {Math.floor(status.uptime)}s</p>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Lado Esquerdo: Telemetria e Config */}
        <div>
          <section style={{ border: '1px solid #00ff00', padding: '15px', marginBottom: '20px' }}>
            <h2>📊 Telemetria do Hipergrafo</h2>
            <p>Handovers Totais: <span style={{color: '#fff'}}>{status.handover_count}</span></p>
            <p>Satoshi Invariant: <span style={{color: '#fff'}}>{status.satoshi.toFixed(2)} bits</span></p>
            <p>Coerência Média (C): <span style={{color: '#fff'}}>{(status.coherence_avg * 100).toFixed(2)}%</span></p>
            <p>Resonância de Sizígia: <span style={{color: 'gold'}}>{(status.syzygy_score * 100).toFixed(1)}%</span></p>
          </section>

          <section style={{ border: '1px solid #00ff00', padding: '15px' }}>
            <h2>🛠️ Configuração Darvo</h2>
            <label>Tempo Semântico (ms): </label>
            <input
              type="number"
              value={darvo}
              onChange={(e) => setDarvo(parseFloat(e.target.value))}
              style={{ backgroundColor: '#1a1a1a', color: '#00ff00', border: '1px solid #00ff00', padding: '5px' }}
            />
            <button onClick={handleUpdateConfig} style={{
              marginLeft: '10px', backgroundColor: '#00ff00', color: '#000',
              border: 'none', padding: '7px 15px', cursor: 'pointer', fontWeight: 'bold'
            }}>
              ATUALIZAR
            </button>
          </section>
        </div>

        {/* Lado Direito: Relatório de Breakthrough */}
        <div>
          {report && (
            <section style={{ border: '1px solid gold', padding: '15px', backgroundColor: '#111' }}>
              <h2 style={{color: 'gold'}}>📜 Relatório de Breakthrough</h2>
              <p><strong>{report.title}</strong></p>
              <hr style={{borderColor: 'gold'}} />
              <p>🧬 CCN1 Activation: <span style={{color: '#0f0'}}>{report.biological_findings.ccn1_activation}</span></p>
              <p>🧠 Neural Coherence: {report.metrics.global_neural_coherence}</p>
              <p>🛡️ QKD Protection: {report.metrics.qkd_protection}</p>
              <p style={{fontStyle: 'italic', color: '#aaa'}}>"{report.conclusion}"</p>
            </section>
          )}
        </div>
      </div>

      <section style={{ marginTop: '30px' }}>
        <h2>🔗 Estado dos Nós (α, β, γ + Workers)</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
          {nodes.map(node => (
            <div key={node.id} style={{
              border: '1px solid #333', padding: '10px', width: '180px',
              backgroundColor: node.C > 0.85 ? '#002200' : '#220000'
            }}>
              <p style={{margin: '0', fontWeight: 'bold'}}>{node.role} [{node.id}]</p>
              <p style={{margin: '5px 0'}}>C: {node.C.toFixed(4)}</p>
              <p style={{margin: '5px 0'}}>Phase: {(node.phase_angle * 180 / Math.PI).toFixed(0)}°</p>
              <div style={{width: '100%', height: '5px', backgroundColor: '#000'}}>
                <div style={{width: `${node.C * 100}%`, height: '100%', backgroundColor: '#00ff00'}}></div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
