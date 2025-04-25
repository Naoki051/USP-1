from sklearn.datasets import make_moons
from rede import treinar_mlp, feedforward
import numpy as np
import matplotlib.pyplot as plt

# Gerando dados com make_moons
X, y = make_moons(n_samples=200, noise=0.2, random_state=42)
X = X.T  # Transpor para ficar (features, amostras)
Y = y.reshape(1, -1)  # Ajustar Y para (1, amostras)

# Estrutura da MLP
estrutura_camadas = [2, 3, 1]

# Treinamento
parametros_treinados, custos_treinamento = treinar_mlp(
    estrutura_camadas, X, Y, num_epocas=3000, taxa_aprendizado=0.8, print_custo=False
)

# Teste
memoria_cache_teste = feedforward(X, parametros_treinados)
previsoes = memoria_cache_teste['A' + str(len(estrutura_camadas) - 1)]
previsoes_binarias = (previsoes > 0.5).astype(int)

print("\nAcurácia:", np.mean(previsoes_binarias == Y))

# Plot do erro
plt.figure(figsize=(10, 6))
plt.plot(range(len(custos_treinamento)), custos_treinamento)
plt.xlabel('Épocas')
plt.ylabel('MSE (Erro Quadrático Médio)')
plt.title('MSE ao Longo do Treinamento com Moons')
plt.grid(True)
plt.show()
