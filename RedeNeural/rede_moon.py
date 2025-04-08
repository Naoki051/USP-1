import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

# -- Suas funções aqui (ativação, derivada_ativacao, inicializacao_dos_pesos, feedforward, backpropagation) --

def ativacao(x):
    return np.tanh(x)

def derivada_ativacao(x):
    return 1 - np.tanh(x)**2

def inicializacao_dos_pesos(num_entrada,num_neuronios,use_bias = True):
    pesos = [[np.random.uniform(-1, 1)*0.01 for _ in range(num_neuronios)] for _ in range(num_entrada)]
    bias = [np.random.uniform(-1, 1)*0.01 if use_bias else 0.0 for _ in range(num_neuronios)]
    return pesos, bias

def feedforward(entradas, pesos, biases):
    saidas = []
    somatorio = []
    num_neuronios = len(pesos[0])
    for j in range(num_neuronios):
        soma = sum(entradas[i]*pesos[i][j] for i in range(len(entradas))) + biases[j]
        somatorio.append(soma)
        saidas.append(ativacao(soma))
    return somatorio, saidas

def backpropagation(entradas, pesos_oculta, biases_oculta, pesos_saida,biases_saida, alvos, taxa_aprendizagem):
    somatorio_entrada_oculta, saidas_oculta = feedforward(entradas,pesos_oculta,biases_oculta)
    somatorio_entrada_saida, saidas = feedforward(saidas_oculta,pesos_saida,biases_saida)

    erros_saida = [s - a for s, a in zip(saidas, alvos)]

    deltas_saida = [erros_saida[i] * derivada_ativacao(somatorio_entrada_saida[i])
                    for i in range(len(erros_saida))]

    # Cálculo dos deltas da camada oculta
    num_neuronios_oculta = len(saidas_oculta)
    num_neuronios_saida = len(deltas_saida)
    delta_oculta = [0.0] * num_neuronios_oculta

    for i in range(num_neuronios_oculta):
        somatorio = 0
        for j in range(num_neuronios_saida):
            somatorio += pesos_saida[i][j] * deltas_saida[j]
        delta_oculta[i] = somatorio * derivada_ativacao(somatorio_entrada_oculta[i])

    # Ajuste dos pesos da camada de saída
    novos_pesos_saida = [[0.0] * num_neuronios_saida for _ in range(num_neuronios_oculta)]
    for i in range(num_neuronios_oculta):
        for j in range(num_neuronios_saida):
            novos_pesos_saida[i][j] = pesos_saida[i][j] - taxa_aprendizagem * saidas_oculta[i] * deltas_saida[j]

    # Ajuste dos biases da camada de saída
    novos_biases_saida = [b - taxa_aprendizagem * d for b, d in zip(biases_saida, deltas_saida)]

    # Ajuste dos pesos da camada oculta
    num_entrada = len(entradas)
    novos_pesos_oculta = [[0.0] * num_neuronios_oculta for _ in range(num_entrada)]
    for i in range(num_entrada):
        for j in range(num_neuronios_oculta):
            novos_pesos_oculta[i][j] = pesos_oculta[i][j] - taxa_aprendizagem * entradas[i] * delta_oculta[j]

    # Ajuste dos biases da camada oculta
    novos_biases_oculta = [b - taxa_aprendizagem * d for b, d in zip(biases_oculta, delta_oculta)]

    return novos_pesos_oculta, novos_biases_oculta, novos_pesos_saida, novos_biases_saida

def treinamento(entradas_treinamento, alvos_treinamento, num_neuronios_oculta, num_epocas, taxa_aprendizagem):
    """Função para treinar a rede neural (aceita listas como entrada)."""
    num_entrada = len(entradas_treinamento[0])
    num_saida = len(alvos_treinamento[0]) if isinstance(alvos_treinamento[0], list) else 1

    # Inicialização dos pesos e biases
    pesos_oculta, biases_oculta = inicializacao_dos_pesos(num_entrada, num_neuronios_oculta)
    pesos_saida, biases_saida = inicializacao_dos_pesos(num_neuronios_oculta, num_saida)

    historico_erros = []

    for epoca in range(num_epocas):
        erro_total = 0
        for i in range(len(entradas_treinamento)):
            entrada = entradas_treinamento[i]
            alvo = alvos_treinamento[i] if isinstance(alvos_treinamento[i], list) else [alvos_treinamento[i]]

            # Backpropagation
            pesos_oculta, biases_oculta, pesos_saida, biases_saida = backpropagation(
                entrada, pesos_oculta, biases_oculta, pesos_saida, biases_saida, alvo, taxa_aprendizagem
            )

            # Feedforward para calcular o erro
            _, saidas = feedforward(feedforward(entrada, pesos_oculta, biases_oculta)[1], pesos_saida, biases_saida)
            erro = np.mean((np.array(saidas) - np.array(alvo))**2)  # Usar NumPy para o cálculo do erro
            erro_total += erro

        erro_medio = erro_total / len(entradas_treinamento)
        historico_erros.append(erro_medio)
        print(f"Época {epoca+1}/{num_epocas}, Erro Médio: {erro_medio:.6f}")

    return pesos_oculta, biases_oculta, pesos_saida, biases_saida, historico_erros


if __name__ == '__main__':
    # Gerar um dataset mais elaborado com make_moons
    X, y = make_moons(n_samples=300, noise=0.25, random_state=42)
    y = y.reshape(-1, 1)  # Reformatar os rótulos para ter uma coluna

    # Dividir os dados em treinamento e teste
    X_train_np, X_test_np, y_train_np, y_test_np = train_test_split(X, y, test_size=0.3, random_state=42)

    # Converter para listas
    entradas_treinamento = X_train_np.tolist()
    alvos_treinamento = y_train_np.tolist()
    entradas_teste = X_test_np.tolist()
    alvos_teste = y_test_np.tolist()

    # Hiperparâmetros
    num_neuronios_oculta = 10
    num_epocas = 500
    taxa_aprendizagem = 0.05

    # Treinamento da rede neural
    pesos_oculta_treinado, biases_oculta_treinado, pesos_saida_treinado, biases_saida_treinado, historico_erros = treinamento(
        entradas_treinamento, alvos_treinamento, num_neuronios_oculta, num_epocas, taxa_aprendizagem
    )

    print("\nTreinamento Concluído!")

    # Teste da rede treinada e cálculo do erro quadrático médio médio
    print("\nTestando a Rede:")
    erros_qm_teste = []
    for i in range(len(entradas_teste)):
        entrada = entradas_teste[i]
        alvo = alvos_teste[i]
        _, saidas_oculta = feedforward(entrada, pesos_oculta_treinado, biases_oculta_treinado)
        _, saida_final = feedforward(saidas_oculta, pesos_saida_treinado, biases_saida_treinado)
        erro_qm = np.mean((np.array(saida_final) - np.array(alvo))**2)
        erros_qm_teste.append(erro_qm)

    erro_medio_teste = np.mean(erros_qm_teste)
    print(f"Erro Quadrático Médio no Conjunto de Teste: {erro_medio_teste:.6f}")

    # Plotar o histórico de erros médios durante o treinamento
    import matplotlib.pyplot as plt
    plt.plot(historico_erros)
    plt.xlabel('Época')
    plt.ylabel('Erro Médio (Treinamento)')
    plt.title('Histórico de Erros durante o Treinamento')
    plt.grid(True)
    plt.show()