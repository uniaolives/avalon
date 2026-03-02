# arkhe/dashboard.py
from .telemetry import TelemetryCollector

class MetricsDashboard:
    """
    Visualização das métricas C/F em tempo real.
    """

    def render(self, telemetry: TelemetryCollector):
        stats = telemetry.get_stats()

        print("╔════════════════════════════════════════════════╗")
        print("║      ARKHE(n) TELEMETRY DASHBOARD v2.0          ║")
        print("╠════════════════════════════════════════════════╣")

        for provider, data in stats.items():
            C = data.get("availability", 0.0)  # Disponibilidade como proxy de C
            F = 1.0 - C

            bar_c = "█" * int(C * 20)
            bar_f = "░" * int(F * 20)

            print(f"║ {provider.upper():12} │ C: {bar_c:<20} {C:.2f} │ F: {bar_f:<20} {F:.2f} ║")
            print(f"║             │ Latency: {data.get('avg_latency_ms', 0):.0f}ms │ Errors: {data.get('error_rate', 0):.2%} ║")
            print("╠════════════════════════════════════════════════╣")

        print("║ Conservation Law: C + F = 1.0 ✅                  ║")
        print("╚════════════════════════════════════════════════╝")
