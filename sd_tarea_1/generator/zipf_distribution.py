import numpy as np

def generate_zipf_dataset_distribution(dataset, max_iterations, seed=123, a=1.5):
    """
    Devuelve una lista de tamaño max_iterations con índices (0..n-1)
    muestreados según una Zipf truncada a los primeros n ranks.
    """
    rng = np.random.default_rng(seed)
    n = len(dataset)
    ranks = np.arange(1, n+1)           # 1,2,...,n
    probs = 1.0 / (ranks ** a)          # p_k ∝ 1 / k^a
    probs /= probs.sum()                # normalizar

    # muestreo con reemplazo según p_k
    indices = rng.choice(n, size=max_iterations, replace=True, p=probs)
    indices = indices.tolist()
    
    print(f"[Status] Zipf distribution generated successfully")
    
    return indices
