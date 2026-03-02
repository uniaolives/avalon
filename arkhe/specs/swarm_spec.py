import numpy as np

class ArkheDroneSpec:
    def __init__(self, id, position):
        self.id = id
        self.pos = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.coherence = 1.0

    def update_physics(self, neighbors, target_geo):
        # 1. Separação (Evitar colisão)
        separation = np.zeros(2)
        for n in neighbors:
            diff = self.pos - n.pos
            dist = np.linalg.norm(diff)
            if dist > 0:
                separation += diff / dist**2

        # 2. Alinhamento (Mimetismo de velocidade)
        if neighbors:
            alignment = np.mean([n.velocity for n in neighbors], axis=0)
        else:
            alignment = np.zeros(2)

        # 3. Coesão (Manter o enxame junto)
        if neighbors:
            cohesion = np.mean([n.pos for n in neighbors], axis=0) - self.pos
        else:
            cohesion = np.zeros(2)

        # 4. Missão (Target: Cristo Redentor / Pão de Açúcar)
        mission_pull = target_geo - self.pos

        # Atualização de estado
        self.velocity += (separation + alignment + cohesion + mission_pull) * 0.1
        self.pos += self.velocity

        # Reportar dados ao GLP
        return {"id": self.id, "telemetry": self.pos, "C": self.coherence}

if __name__ == "__main__":
    print("🚁 Initializing Swarm Specification Simulation...")
    swarm = [ArkheDroneSpec(i, [np.random.rand()*10, np.random.rand()*10]) for i in range(12)]
    target = np.array([50.0, 50.0])

    for _ in range(10):
        for drone in swarm:
            neighbors = [d for d in swarm if d != drone and np.linalg.norm(d.pos - drone.pos) < 5.0]
            drone.update_physics(neighbors, target)

    print(f"Swarm final position (avg): {np.mean([d.pos for d in swarm], axis=0)}")
    print("∞")
