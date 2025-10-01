import numpy
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import norm

# Mapeo ORIGINAL que transforma la distribución gaussiana
# Los valores más probables de la gaussiana (5,6) se mapean a clases específicas
RIGHT_FREQUENCIES = {
    1: 10,  # [Society & Culture]      -> #1  Politics & Government 
    2: 7,   # [Science & Mathematics]  -> #2  Business & Finance
    3: 5,   # [Health]                 -> #3  Computers & Internet
    4: 2,   # [Education & Reference]  -> #4  Science & Mathematics
    5: 6,   # [Computers & Internet]   -> #5  Sports
    6: 8,   # [Sports]                 -> #6  Entertainment & Music
    7: 1,   # [Business & Finance]     -> #7  Society & Culture
    8: 4,   # [Entertainment & Music]  -> #8  Education & Reference
    9: 9,   # [Family & Relationships] -> #9  Family & Relationships
    10: 3   # [Politics & Government]  -> #10 Health
}

def graph_distribution(distribution, graph_title="Distribución observada"):
    counter = Counter(distribution)
    values = sorted(counter.keys())
    frequencies = [counter[i] for i in values]
    
    plt.bar(values, frequencies, width=0.6, alpha=0.7, label="Datos observados")
    
    mu, sigma = numpy.mean(distribution), numpy.std(distribution)
    x = numpy.linspace(1, 10, 100)
    y = norm.pdf(x, mu, sigma) * len(distribution)
    
    plt.plot(x, y, 'r-', linewidth=2, label=f'Normal ajustada\nμ={mu:.2f}, σ={sigma:.2f}')
    plt.xlabel("Class Index")
    plt.ylabel("Frecuencia")
    plt.title(graph_title)
    plt.xticks(range(1, 11))
    plt.legend()
    plt.show()

def generate_gaussian_dataset_distribution(dataset, MAX_ITERATIONS, SEED):

    RNG = numpy.random.default_rng(SEED)
    
    try:
        # 1. Primero generamos la misma distribución gaussiana transformada que en tu versión original
        gauss_numbers = []
        while len(gauss_numbers) < MAX_ITERATIONS:
            raw_idxs = RNG.normal(loc=5.5, scale=2.0, size=MAX_ITERATIONS)
            idxs = [int(round(i)) for i in raw_idxs if 1 <= round(i) <= 10]
            gauss_numbers.extend(idxs)
        
        # Aplicar el mapeo transformador
        transformed_classes = [RIGHT_FREQUENCIES[i] for i in gauss_numbers[:MAX_ITERATIONS]]
        
        # 2. Precomputar índices por clase para acceso rápido
        class_indices = {}
        for class_idx in range(1, 11):
            class_indices[class_idx] = dataset[dataset["class_index"] == class_idx].index.tolist()
        
        # 3. Para cada clase en la distribución transformada, seleccionar una fila aleatoria
        distribution_indices = []
        for class_idx in transformed_classes:
            available_indices = class_indices[class_idx]
            if available_indices:
                selected_idx = RNG.choice(available_indices)
                distribution_indices.append(selected_idx)
            else:
                # Fallback: si no hay datos para esta clase, usar una clase similar
                similar_classes = [cls for cls in range(1, 11) if class_indices[cls]]
                if similar_classes:
                    fallback_class = RNG.choice(similar_classes)
                    selected_idx = RNG.choice(class_indices[fallback_class])
                    distribution_indices.append(selected_idx)
                else:
                    raise Exception("No hay datos disponibles en el dataset")
        
        print(f"[Status] Gaussian distribution generated successfully")
        print(f"    ↳ Target class distribution: {dict(Counter(transformed_classes))}")
        
        return distribution_indices
    
    except Exception as e:
        print(f"[Error] Error generating optimized distribution:\n", e)
        return None

# Mantener función original para comparación
def generate_gaussian_distribution(MAX_ITERATIONS, SEED):
    RNG = numpy.random.default_rng(SEED)

    gauss_distribution = []
    
    try:
        while len(gauss_distribution) < MAX_ITERATIONS:
            raw_idxs = RNG.normal(loc=5.5, scale=2.0, size=MAX_ITERATIONS)
            idxs = [int(round(i)) for i in raw_idxs if 1 <= round(i) <= 10]
            gauss_distribution.extend(idxs)
        
        gauss_distribution = [RIGHT_FREQUENCIES[i] for i in gauss_distribution]
        
        print(f"[Status] Original gaussian distribution generated successfully")
        return gauss_distribution[:MAX_ITERATIONS] 
    
    except Exception as e:
        print(f"[Error] Error generating distribution:\n", e)
        return None