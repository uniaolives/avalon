def emergency_halt():
    """Kill switch imediato < 25ms."""
    print("[HALT] Ativando protocolo de emergência.")
    raise SystemExit("Emergency Halt")
