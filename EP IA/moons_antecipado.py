from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
from rede import treinar_mlp_com_parada_antecipada

X, y = make_moons(n_samples=300, noise=0.25, random_state=42)
X = X.T
Y = y.reshape(1, -1)

# Separando treino e validação
X_treino, X_val, Y_treino, Y_val = train_test_split(X.T, Y.T, test_size=0.2, random_state=42)
X_treino, X_val = X_treino.T, X_val.T
Y_treino, Y_val = Y_treino.T, Y_val.T

# Estrutura da rede
camadas = [2, 3, 1]

# Treinamento com parada antecipada
parametros, custo_treino, custo_val = treinar_mlp_com_parada_antecipada(
    camadas, X_treino, Y_treino, X_val, Y_val,
    num_epocas=3000,
    taxa_aprendizado=0.1,
    paciencia=100,
    print_custo=True
)
plt.figure(figsize=(10, 6))
plt.plot(custo_treino, label="Treinamento")
plt.plot(custo_val, label="Validação")
plt.xlabel("Épocas")
plt.ylabel("Erro MSE")
plt.title("Erro durante o Treinamento com Validação")
plt.legend()
plt.grid(True)
plt.show()