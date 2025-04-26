import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from rede import treinar_mlp_momentum_com_parada_antecipada,treinar_mlp_momentum

# Função para carregar os dados
def carregar_dados(x_path, y_path):
    # Carregar X com genfromtxt e ignorar a última coluna (se for sempre vazia)
    X = np.genfromtxt(x_path, delimiter=',')[:, :-1].T

    # Carregar Y (o restante do seu código para Y permanece o mesmo)
    with open(y_path, 'r') as f:
        y_strings = [linha.strip() for linha in f.readlines()]

    # Converter letras para números 0-25
    y_inteiros = np.array([ord(letra) - ord('A') for letra in y_strings])

    # One-hot encoding para saída (26 classes)
    Y = np.zeros((26, len(y_inteiros)))
    Y[y_inteiros, np.arange(len(y_inteiros))] = 1

    return X, Y

# Carregar dados
X, Y = carregar_dados('CARACTERES COMPLETO\X.txt', 'CARACTERES COMPLETO\Y_letra.txt')

# Separar treino e validação
X_treino, X_val, Y_treino, Y_val = train_test_split(X.T, Y.T, test_size=0.2, random_state=42)
X_treino, X_val = X_treino.T, X_val.T
Y_treino, Y_val = Y_treino.T, Y_val.T

# Definir estrutura da rede
# Você pode mudar o número de neurônios na camada oculta aqui
camadas = [120, 64, 26]  # Exemplo: 64 neurônios na camada oculta

# Treinamento
parametros, custo_treino = treinar_mlp_momentum(
    camadas, X_treino, Y_treino,
    num_epocas=15000,
    taxa_aprendizado=0.1,
    beta=0.5,
    print_custo=True
)

# Plotar erro
plt.figure(figsize=(10, 6))
plt.plot(custo_treino, label="Treinamento")
plt.xlabel("Épocas")
plt.ylabel("Erro MSE")
plt.title("Erro durante o Treinamento")
plt.legend()
plt.grid(True)
plt.show()
