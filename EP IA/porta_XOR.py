from rede import treinar_mlp, feedforward
import numpy as np
import matplotlib.pyplot as plt

# Exemplo de uso porta XOR:
estrutura_camadas = [2, 3, 1]
X_treino = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]).T
Y_treino = np.array([[0, 1, 1, 0]])  # Exemplo de problema XOR

parametros_treinados, custos_treinamento = treinar_mlp(estrutura_camadas, X_treino, Y_treino, num_epocas=20000, taxa_aprendizado=0.95, print_custo=False)

print("\nParâmetros treinados:")
for item in parametros_treinados:
    print(item, ":\n", parametros_treinados[item])

# Testando a rede treinada
memoria_cache_teste = feedforward(X_treino, parametros_treinados)
previsoes = memoria_cache_teste['A' + str(len(estrutura_camadas) - 1)]
print("\nPrevisões após o treinamento:")
print(previsoes[0])
# Plotando o MSE ao longo do treinamento
plt.figure(figsize=(10, 6))
plt.plot(range(len(custos_treinamento)), custos_treinamento)
plt.xlabel('Épocas')
plt.ylabel('MSE (Erro Quadrático Médio)')
plt.title('MSE ao Longo do Treinamento')
plt.grid(True)
plt.show()
