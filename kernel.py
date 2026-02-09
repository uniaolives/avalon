import numpy as np
from scipy.fft import fftn
from skimage.measure import shannon_entropy

class BioSignatureKernel:
    def __init__(self, spatial_res=(10, 10), spectral_bands=8, time_steps=16):
        self.shape = (*spatial_res, spectral_bands, time_steps)

    def _normalize(self, data):
        return (data - np.mean(data)) / (np.std(data) + 1e-8)

    def extract_features(self, raw_data):
        # Redimensiona para o hipercubo esperado
        data = self._normalize(raw_data.reshape(self.shape))

        # DNE (Dynamic Non-Equilibrium): Persistência temporal
        diff_t = np.diff(data, axis=-1)
        dne = np.tanh(np.mean(np.abs(fftn(diff_t))))

        # SSO (Spatial Self-Organization): Entropia espacial relativa
        sso_vals = [shannon_entropy(data[..., b, :]) for b in range(self.shape[2])]
        sso = np.mean(sso_vals) / (np.max(sso_vals) + 1e-8)

        # CDC (Cross-Domain Coupling): Correlação entre bandas
        bands = data.reshape(-1, self.shape[2], self.shape[3]).mean(axis=0)
        cdc = np.abs(np.corrcoef(bands)).mean()

        return {"D": float(dne), "S": float(sso), "C": float(cdc)}
