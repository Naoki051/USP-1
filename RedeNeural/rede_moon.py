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
        if erro_medio<=0.093:
            break
        print(f"Época {epoca+1}/{num_epocas}, Erro Médio: {erro_medio:.6f}")

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
    # Gerar um dataset mais elaborado com make_moons
    X, y = make_moons(n_samples=300, noise=0.25, random_state=42)
    y = y.reshape(-1, 1).tolist()  # Converter para lista de listas

    # Dividir os dados em treinamento, validação e teste
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42) # 0.25 de 0.8 = 0.2 para validação

    entradas_treinamento = X_train.tolist()
    alvos_treinamento = y_train
    entradas_validacao = X_val.tolist()
    alvos_validacao = y_val
    entradas_teste = X_test.tolist()
    alvos_teste = y_test

    # Hiperparâmetros
    num_neuronios_oculta = 10
    num_epocas = 500  # Aumentei o número de épocas para dar chance ao early stopping
    taxa_aprendizagem = 0.05
    paciencia = 20  # Número de épocas sem melhora para parar

    # Treinamento da rede neural com validação antecipada
    melhores_pesos_oculta, melhores_biases_oculta, melhores_pesos_saida, melhores_biases_saida, historico_erros_treinamento, historico_erros_validacao = treinamento_com_validacao(
        entradas_treinamento, alvos_treinamento, entradas_validacao, alvos_validacao, num_neuronios_oculta, num_epocas, taxa_aprendizagem, paciencia
    )

    print("\nTreinamento Concluído (com parada antecipada).")

    # Teste da rede com os melhores pesos encontrados
    print("\nTestando a Rede com os melhores pesos no conjunto de teste:")
    erros_qm_teste = []
    for i in range(len(entradas_teste)):
        entrada = entradas_teste[i]
        alvo = alvos_teste[i]
        _, saidas_oculta = feedforward(entrada, melhores_pesos_oculta, melhores_biases_oculta)
        _, saida_final = feedforward(saidas_oculta, melhores_pesos_saida, melhores_biases_saida)
        erro_qm = np.mean((np.array(saida_final) - np.array(alvo))**2)
        erros_qm_teste.append(erro_qm)

    erro_medio_teste = np.mean(erros_qm_teste)
    print(f"Erro Quadrático Médio no Conjunto de Teste (com parada antecipada): {erro_medio_teste:.6f}")

    # Plotar o histórico de erros
    plt.figure(figsize=(10, 5))
    plt.plot(historico_erros_treinamento, label='Treinamento')
    plt.plot(historico_erros_validacao, label='Validação')
    plt.xlabel('Época')
    plt.ylabel('Erro Médio')
    plt.title('Histórico de Erros durante o Treinamento com Validação')
    plt.legend()
    plt.grid(True)
    plt.show()