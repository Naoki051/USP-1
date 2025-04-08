import numpy as np
import matplotlib.pyplot as plt

def ativacao(x):
    """Função de ativação tangente hiperbólica."""
    return np.tanh(x)
def derivada_ativacao(x):
    """Calcula a derivada da função tangente hiperbólica."""
    return 1 - np.tanh(x)**2

def inicializacao_dos_pesos(num_entrada,num_neuronios,use_bias = True):

    # Inicialização da matriz de pesos com zeros
    pesos = [[0 for _ in range(num_neuronios)] for _ in range(num_entrada)]
    # Inicialização do vetor de viés com zeros
    bias = [0 for _ in range(num_neuronios)]

    for j in range(num_neuronios):
        if use_bias:
            bias[j] = np.random.uniform(-1, 1)*0.01
        else:
            bias[j] = 0.0
        for i in range(num_entrada):
            pesos[i][j] = np.random.uniform(-1, 1)*0.01

    return pesos,bias

def feedforward(entradas, pesos, biases):
    saidas = []
    somatorio = []
    num_neuronios = len(pesos[0])
    for j in range(num_neuronios):
        somatorio.append(0)
        for i in range(len(entradas)):
            somatorio[j] += entradas[i]*pesos[i][j]
        somatorio[j] += biases[j]
        saidas.append(ativacao(somatorio[j]))
    return somatorio, saidas

def backpropagation(entradas, pesos_oculta, biases_oculto, pesos_saida,biases_saida, alvos, taxa_aprendizagem):
    somatorio_entrada_oculta, saidas_oculta = feedforward(entradas,pesos_oculta,biases_oculto)
    somatorio_entrada_saida, saidas = feedforward(saidas_oculta,pesos_saida,biases_saida)

    erros_saida = [s - a for s, a in zip(saidas, alvos)]

    deltas_saida = [erros_saida[i] * derivada_ativacao(somatorio_entrada_saida[i])
                    for i in range(len(erros_saida))]

    
    delta_oculta = [0.0] * len(saidas_oculta)
    num_neuronios_oculta = len(saidas_oculta)
    num_neuronios_saida = len(deltas_saida)


    for i in range(num_neuronios_oculta):
        somatorio = 0
        for j in range(num_neuronios_saida):
            somatorio += pesos_saida[i][j] * deltas_saida[j]
        delta_oculta[i] = somatorio * derivada_ativacao(somatorio_entrada_oculta[i])
    
    novos_pesos_oculta = [[0.0] * len(entradas) for _ in range(num_neuronios_oculta)]
    
    # Ajuste dos pesos da camada oculta
    for j in range(num_neuronios_oculta):
        for i in range(len(entradas)):
            novos_pesos_oculta[j][i] = pesos_oculta[j][i] - taxa_aprendizagem * delta_oculta[j] * entradas[i]
    
    # Ajuste dos biases da camada oculta
    novos_biases_oculta = [biases_oculto[i] - taxa_aprendizagem * delta_oculta[i]
                           for i in range(len(biases_oculto))]

    # Ajuste dos pesos da camada de saída
    num_neuronios_saida = len(alvos)
    num_neuronios_oculta = len(saidas_oculta)
    novos_pesos_saida = [[0.0] * num_neuronios_saida for _ in range(num_neuronios_oculta)]

    for j in range(num_neuronios_oculta):
        for i in range(num_neuronios_saida):
            novos_pesos_saida[j][i] = pesos_saida[j][i] - taxa_aprendizagem * deltas_saida[i] * saidas_oculta[j]


    # Ajuste dos biases da camada de saída
    novos_biases_saida = [biases_saida[i] - taxa_aprendizagem * deltas_saida[i]
                           for i in range(len(biases_saida))]
    return novos_pesos_oculta, novos_biases_oculta, novos_pesos_saida, novos_biases_saida

def treinamento(entradas_treinamento, alvos_treinamento, num_neuronios_oculta, num_epocas, taxa_aprendizagem):
    """Função para treinar a rede neural."""
    num_entrada = len(entradas_treinamento[0])
    num_saida = len(alvos_treinamento[0])

    # Inicialização dos pesos e biases
    pesos_oculta, biases_oculta = inicializacao_dos_pesos(num_entrada, num_neuronios_oculta)
    pesos_saida, biases_saida = inicializacao_dos_pesos(num_neuronios_oculta, num_saida)

    historico_erros = []

    for epoca in range(num_epocas):
        erro_total = 0
        for i in range(len(entradas_treinamento)):
            entrada = entradas_treinamento[i]
            alvo = alvos_treinamento[i]

            # Backpropagation
            pesos_oculta, biases_oculta, pesos_saida, biases_saida = backpropagation(
                entrada, pesos_oculta, biases_oculta, pesos_saida, biases_saida, alvo, taxa_aprendizagem
            )

            # Feedforward para calcular o erro
            _, saidas = feedforward(feedforward(entrada, pesos_oculta, biases_oculta)[1], pesos_saida, biases_saida)
            erro = np.mean((saidas - alvo)**2)
            erro_total += erro

        erro_medio = erro_total / len(entradas_treinamento)
        historico_erros.append(erro_medio)

    return pesos_oculta, biases_oculta, pesos_saida, biases_saida, historico_erros

if __name__ == '__main__':
    # Dados de exemplo para treinamento (problema XOR)
    entradas_treinamento = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    alvos_treinamento = np.array([[0], [1], [1], [0]])

    # Hiperparâmetros
    num_neuronios_oculta = 2
    num_epocas = 500
    taxa_aprendizagem = 0.1

    # Treinamento da rede neural
    pesos_oculta_treinado, biases_oculta_treinado, pesos_saida_treinado, biases_saida_treinado, historico_erros = treinamento(
        entradas_treinamento, alvos_treinamento, num_neuronios_oculta, num_epocas, taxa_aprendizagem
    )

    print("\nTreinamento Concluído!")

    # Teste da rede treinada e impressão do erro quadrático médio
    print("\nTestando a Rede:")
    for i in range(len(entradas_treinamento)):
        entrada = entradas_treinamento[i]
        alvo = alvos_treinamento[i]
        _, saidas_oculta = feedforward(entrada, pesos_oculta_treinado, biases_oculta_treinado)
        _, saida_final = feedforward(saidas_oculta, pesos_saida_treinado, biases_saida_treinado)
        erro_quadratico_medio = np.mean((saida_final - alvo)**2)
        print(f"Entrada: {entrada}, Saída Esperada: {alvo}, Saída Obtida: {saida_final}, Erro QM: {erro_quadratico_medio:.6f}")

    # Plotar o histórico de erros
    plt.plot(historico_erros)
    plt.xlabel('Época')
    plt.ylabel('Erro Médio')
    plt.title('Histórico de Erros durante o Treinamento')
    plt.grid(True)
    plt.show()