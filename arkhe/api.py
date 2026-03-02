# arkhe/api.py
"""
Secure Admin Console API (v10.0)
Orchestrates neuro-mapping, security reports, and sovereign governance.
"""

from aiohttp import web
import json
import time
import numpy as np
from typing import Dict, Any
from .report import SyzygyReportGenerator

class AdminAPI:
    """
    API REST para o Console Administrativo do Arkhe(n) OS.
    """
    def __init__(self, hypergraph, qkd_manager, consensus_engine, neuro_mapper=None):
        self.hg = hypergraph
        self.qkd = qkd_manager
        self.consensus = consensus_engine
        self.neuro = neuro_mapper
        self.report_gen = SyzygyReportGenerator(neuro_mapper, qkd_manager) if neuro_mapper else None
        self.start_time = time.time()

    async def get_status(self, request):
        """Retorna o status geral da rede."""
        data = {
            "uptime": time.time() - self.start_time,
            "handover_count": self.hg.handover_count,
            "satoshi": float(self.hg.satoshi),
            "nu_obs": float(self.hg.nu_obs),
            "r_rh": float(self.hg.r_rh),
            "coherence_avg": float(np.mean([n.C for n in self.hg.nodes])),
            "syzygy_score": float(self.consensus.voting_threshold),
            "neuro_active": self.neuro is not None,
            "qkd_lock": "ACTIVE"
        }
        return web.json_response(data)

    async def get_nodes(self, request):
        """Retorna lista de nós com metadados de fase."""
        nodes_data = []
        target_ids = [0, 1, 2] + list(range(3, 10))
        for i in target_ids:
            if i < len(self.hg.nodes):
                n = self.hg.nodes[i]
                nodes_data.append({
                    "id": n.id,
                    "C": float(n.C),
                    "F": float(n.F),
                    "phi": float(n.phi),
                    "phase_angle": float(n.x % (2*np.pi)), # Simulado
                    "role": "Validator" if i < 3 else "Worker"
                })
        return web.json_response(nodes_data)

    async def get_report(self, request):
        """Retorna o Relatório de Breakthrough de Sizígia."""
        if not self.report_gen:
            return web.json_response({"error": "Report generator not initialized"}, status=503)
        return web.json_response(self.report_gen.generate_executive_summary())

    async def post_config(self, request):
        """Atualiza parâmetros do protocolo Darvo/Coerência."""
        try:
            body = await request.json()
            if "darvo_time" in body:
                self.hg.darvo = body["darvo_time"]
                self.qkd.update_darvo(self.hg.darvo)
            return web.json_response({"status": "updated", "darvo": self.hg.darvo})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)

    def setup_routes(self, app):
        app.router.add_get('/api/status', self.get_status)
        app.router.add_get('/api/nodes', self.get_nodes)
        app.router.add_get('/api/report', self.get_report)
        app.router.add_post('/api/config', self.post_config)
