from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from kernel import BioSignatureKernel
from quantum_logic import PersistentOrderOracle

app = FastAPI(title="QCN Node - POP Protocol")
kernel = BioSignatureKernel()
oracle = PersistentOrderOracle()

class ScanPayload(BaseModel):
    node_id: str
    spectral_data: list
    metadata: dict

@app.post("/qhttp/scan")
async def process_scan(payload: ScanPayload):
    try:
        # 1. Processamento Clássico (Kernel)
        features = kernel.extract_features(np.array(payload.spectral_data))

        # 2. Processamento Quântico (Oracle)
        # Using the methods from the implemented PersistentOrderOracle in quantum_logic.py
        psi_po = oracle.execute_and_filter(features)

        return {
            "node_status": "entangled",
            "psi_po": psi_po,
            "features": features,
            "action": "AMPLIFY" if psi_po > 0.8 else "STOCHASTIC_NOISE"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
