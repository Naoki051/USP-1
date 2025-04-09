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

def calcular_erro(saidas, alvos):
    """Calcula o erro quadrático médio."""
    erro = sum((s - a)**2 for s, a in zip(saidas, alvos)) / len(saidas)
    return erro

def treinamento_com_validacao(entradas_treinamento, alvos_treinamento, entradas_validacao, alvos_validacao, num_neuronios_oculta, num_epocas, taxa_aprendizagem, paciencia=10):
    """Função para treinar a rede neural com validação antecipada."""
    num_entrada = len(entradas_treinamento[0])
    num_saida = len(alvos_treinamento[0]) if isinstance(alvos_treinamento[0], list) else 1

    # Inicialização dos pesos e biases
    pesos_oculta, biases_oculta = inicializacao_dos_pesos(num_entrada, num_neuronios_oculta)
    pesos_saida, biases_saida = inicializacao_dos_pesos(num_neuronios_oculta, num_saida)

    historico_erros_treinamento = []
    historico_erros_validacao = []
    melhor_erro_validacao = float('inf')
    melhores_pesos_oculta = None
    melhores_biases_oculta = None
    melhores_pesos_saida = None
    melhores_biases_saida = None
    contador_paciencia = 0

    for epoca in range(num_epocas):
        erro_total_treinamento = 0
        for i in range(len(entradas_treinamento)):
            entrada = entradas_treinamento[i]
            alvo = alvos_treinamento[i] if isinstance(alvos_treinamento[i], list) else [alvos_treinamento[i]]

            # Backpropagation
            pesos_oculta, biases_oculta, pesos_saida, biases_saida = backpropagation(
                entrada, pesos_oculta, biases_oculta, pesos_saida, biases_saida, alvo, taxa_aprendizagem
            )

            # Feedforward para calcular o erro de treinamento
            _, saidas_treinamento = feedforward(feedforward(entrada, pesos_oculta, biases_oculta)[1], pesos_saida, biases_saida)
            erro_total_treinamento += calcular_erro(saidas_treinamento, alvo)

        erro_medio_treinamento = erro_total_treinamento / len(entradas_treinamento)
        historico_erros_treinamento.append(erro_medio_treinamento)

        # Avaliação no conjunto de validação
        erro_total_validacao = 0
        for i in range(len(entradas_validacao)):
            entrada_validacao = entradas_validacao[i]
            alvo_validacao = alvos_validacao[i] if isinstance(alvos_validacao[i], list) else [alvos_validacao[i]]
            _, saidas_validacao = feedforward(feedforward(entrada_validacao, pesos_oculta, biases_oculta)[1], pesos_saida, biases_saida)
            erro_total_validacao += calcular_erro(saidas_validacao, alvo_validacao)

        erro_medio_validacao = erro_total_validacao / len(entradas_validacao)
        historico_erros_validacao.append(erro_medio_validacao)

        print(f"Época {epoca+1}/{num_epocas}, Erro Treinamento: {erro_medio_treinamento:.6f}, Erro Validação: {erro_medio_validacao:.6f}")

        # Critério de parada antecipada
        if erro_medio_validacao < melhor_erro_validacao:
            melhor_erro_validacao = erro_medio_validacao
            melhores_pesos_oculta = [list(p) for p in pesos_oculta] # Salvar uma cópia
            melhores_biases_oculta = list(biases_oculta)
            melhores_pesos_saida = [list(p) for p in pesos_saida]
            melhores_biases_saida = list(biases_saida)
            contador_paciencia = 0
        else:
            contador_paciencia += 1
            if contador_paciencia >= paciencia:
                print(f"Parada antecipada acionada na época {epoca+1}.")
                break

    return melhores_pesos_oculta, melhores_biases_oculta, melhores_pesos_saida, melhores_biases_saida, historico_erros_treinamento, historico_erros_validacao


if __name__ == '__main__':
    # Dados de exemplo para treinamento (problema XOR)
    entradas_treinamento = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    alvos_treinamento = np.array([[0], [1], [1], [0]])

    # Hiperparâmetros
    num_neuronios_oculta = 2
    num_epocas = 10000
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