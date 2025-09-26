
import numpy
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import norm

# Indexes near 5.5 are more likely to be selected
# So this help to fix the frequency of every category in order to be "more accurate"
# Example: Now [Entertainment & Music] will have the frequency corresponding to position 6 in the normal distribution
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
    
    # Graficar histograma (distribución observada)
    plt.bar(values, frequencies, width=0.6, alpha=0.7, label="Datos observados")
    
    # Ajustar una normal a tus datos
    mu, sigma = numpy.mean(distribution), numpy.std(distribution)
    x = numpy.linspace(1, 10, 100)
    y = norm.pdf(x, mu, sigma) * len(distribution)
    
    plt.plot(x, y, 'r-', linewidth=2, label=f'Normal ajustada\nμ={mu:.2f}, σ={sigma:.2f}')
    plt.xlabel("Valores")
    plt.ylabel("Frecuencia")
    plt.title(graph_title)
    plt.xticks(range(1, 11))
    plt.legend()
    plt.show()
    
    
def generate_gaussian_distribution(MAX_ITERATIONS, SEED):
    
    RNG = numpy.random.default_rng(SEED)

    gauss_distribution = []
    
    try:
        while len(gauss_distribution) < MAX_ITERATIONS:
            
            raw_idxs = RNG.normal(loc=5.5, scale=2.0, size=MAX_ITERATIONS)
            
            idxs = [int(round(i)) for i in raw_idxs if 1 <= round(i) <= 10]
            
            gauss_distribution.extend(idxs)
            

        
        gauss_distribution = [RIGHT_FREQUENCIES[i] for i in gauss_distribution]
        
        print(f"[Status] gaussian distribution generated successfully")
        return gauss_distribution[:MAX_ITERATIONS] 
    
    except Exception as e:
        print(f"[Error] Error generating distribution:\n", e)
        return None
        


if __name__ == "__main__":
    
    gauss_distribution = generate_gaussian_distribution(MAX_ITERATIONS=100000)
    
    graph_distribution(gauss_distribution)
    
    