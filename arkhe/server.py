# arkhe/server.py
"""
Arkhe(n) OS Admin Server
Serves the API and Admin Dashboard.
"""

from aiohttp import web
import asyncio
from .api import AdminAPI

async def start_admin_server(hypergraph, qkd_manager, consensus_engine, neuro_mapper=None, port=8080):
    app = web.Application()

    admin_api = AdminAPI(hypergraph, qkd_manager, consensus_engine, neuro_mapper)
    admin_api.setup_routes(app)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)

    print(f"🚀 [SERVER] Console Administrativo v10.0 iniciado em http://localhost:{port}")
    await site.start()

    return runner
