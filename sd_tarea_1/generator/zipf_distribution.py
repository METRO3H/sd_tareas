import numpy as np

def generate_zipf_dataset_distribution(dataset, max_iterations, seed=123, a=1.5):

    rng = np.random.default_rng(seed)
    n = len(dataset)
    ranks = np.arange(1, n+1)
    probs = 1.0 / (ranks ** a)
    probs /= probs.sum()                

    # muestreo con reemplazo según p_k
    indices = rng.choice(n, size=max_iterations, replace=True, p=probs)
    indices = indices.tolist()
    
    print(f"[Status] Zipf distribution generated successfully")
    
    return indices
