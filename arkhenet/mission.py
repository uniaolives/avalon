# mission.py
import asyncio
import numpy as np
from arkhenet_core import DroneNode
from glp_interface import GLPModel
from nanoparticle_sensor import NanoSensor

async def main():
    print("🚀 Initializing ArkheNet Mission...")
    # Inicializa GLP (meta‑consciência)
    glp = GLPModel(model_path="glp_llama1b.pt", input_dim=128, n_meta_neurons=16)

    # Cria drones
    drone1 = DroneNode(1001, (0,0,0))
    drone2 = DroneNode(1002, (10,5,0))
    drone3 = DroneNode(1003, (5,10,0))
    drones = [drone1, drone2, drone3]

    # Define alvos
    for d in drones:
        d.target_position = np.array([50, 50, 20])

    # Sensor biomimético
    sensor = NanoSensor("sensor_01", target_marker="cancer_cell")

    # Simula ambiente
    environment = {"cancer_cell": 0.9, "temperature": 37.0}

    for step in range(20): # Reduced steps for simulation
        # Cada drone: sense → process → act
        for d in drones:
            data = d.sense()
            proc = d.process(data)
            d.act(proc)
            d.fly_towards_target(0.1)

        # Sensor detecta e libera payload se houver
        stim = sensor.detect(environment)
        if stim > 0.8:
            released = sensor.release_cargo(stim)
            if released:
                print(f"  Step {step}: Sensor {sensor.id} liberou cargo: {released}")

        # Coleta meta‑neurônios (simula ativações dos drones)
        activations = np.array([d.node.coherence for d in drones] + [sensor.coherence])
        # Padding para input_dim 128
        pad = np.zeros(128 - len(activations))
        full_activations = np.concatenate([activations, pad])
        meta = glp.encode(full_activations)

        if step % 5 == 0:
            print(f"  Step {step}: meta‑neurônios = {meta[:3]}...")

    print("🏁 Mission Simulation Complete.")

if __name__ == "__main__":
    asyncio.run(main())
