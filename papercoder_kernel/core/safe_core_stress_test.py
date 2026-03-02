import time
import numpy as np
import hashlib

class SafeCoreStressTest:
    def __init__(self):
        # Axioma Fundamental
        self.phi_ratio = (1 + 5**0.5) / 2 # 1.618

        # Limiares de Governança
        self.C_THRESHOLD = 0.847
        self.PHI_LIMIT = 0.1
        self.SYNC_FREQ = 40.0 # Hz (25ms por ciclo)

        # Estado Inicial
        self.coherence = 0.98
        self.phi_q = 0.0063
        self.is_active = True
        self.start_time = time.time()

    def generate_trace_hash(self, val):
        return hashlib.sha256(str(val).encode()).hexdigest()[:16]

    def run_simulation(self):
        print(f"🚀 [INIT] Safe Core Stress Test - Shard 0")
        print(f"Axioma Ativo: x² = x + 1 | Alvo: {self.SYNC_FREQ}Hz\n")

        # Injeção de Ruído (O Ataque)
        noise_level = 0.01

        cycle = 0
        try:
            while self.is_active:
                cycle_start = time.time()

                # Simulação de Decaimento de Coerência (Ataque Exponencial)
                noise_level *= 1.45
                self.coherence -= noise_level * np.random.random()
                self.phi_q += (noise_level * 0.5) # Simula desequilíbrio de integração

                # Verificação de Governança Arkhe(N)
                status = "NOMINAL"
                violation = None

                if self.coherence < self.C_THRESHOLD:
                    status = "CRITICAL"
                    violation = "COHERENCE_COLLAPSE"
                elif self.phi_q > self.PHI_LIMIT:
                    status = "CRITICAL"
                    violation = "PHI_OVERFLOW"

                # Telemetria
                ts = time.time() - self.start_time
                h = self.generate_trace_hash(self.coherence)
                print(f"T+{ts:.4f}s | Cycle {cycle:02d} | C: {self.coherence:.4f} | Φ: {self.phi_q:.4f} | Hash: {h} | Status: {status}")

                # O KILL SWITCH (Interrupção Topológica)
                if status == "CRITICAL":
                    self.trigger_kill_switch(violation, ts)
                    break

                cycle += 1
                # Mantém a frequência de 40Hz
                time.sleep(max(0, (1/self.SYNC_FREQ) - (time.time() - cycle_start)))

        except KeyboardInterrupt:
            print("\n[STOP] Teste interrompido pelo usuário.")

    def trigger_kill_switch(self, reason, timestamp):
        # O colapso da função de onda para estado seguro
        self.is_active = False
        print("\n" + "!"*50)
        print(f"!!! KILL SWITCH ACIONADO !!!")
        print(f"Motivo: {reason}")
        print(f"Latência de Resposta: {(time.time() - self.start_time - timestamp)*1000:.2f}ms")
        print(f"Estado Final: Desentrelaçamento Seguro Concluído.")
        print("!"*50)

# Execução do Teste
if __name__ == "__main__":
    tester = SafeCoreStressTest()
    tester.run_simulation()
