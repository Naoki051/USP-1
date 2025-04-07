import numpy as np

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

def backpropagation(entradas, pesos_oculta, biases_oculto, pesos_saida,biases_saida, alvos):
    somatorio_oculta, saidas_oculta = feedforward(entradas,pesos_oculta,biases_oculto)
    somatorio_saida, saidas = feedforward(saidas_oculta,pesos_saida,biases_saida)

    erros_saida = []
    for i in range(saidas):
        erros_saida.append(saidas[i]-alvos[i])

    deltas_saida = []
    for i in range(entradas):
        deltas_saida.append(erros_saida[i]*derivada_ativacao(entradas[i]))
    
    delta_oculta=[]
    num_neuronios_saida = len(pesos_saida[0])
    num_neuronios_oculta = len(pesos_saida)
    for k in range(num_neuronios_saida):
        somatorio = 0
        for j in range(num_neuronios_oculta):
            somatorio += pesos_oculta[k][j]*deltas_saida[k]
        delta_oculta.append(somatorio*derivada_ativacao(entradas[k]))
