import numpy as np

def tanh(x):
    """Função de ativação tangente hiperbólica."""
    return np.tanh(x)

def derivada_tanh(x):
    """Derivada da função de ativação tangente hiperbólica."""
    return 1 - np.tanh(x)**2

def backpropagation(saida_desejada, saida_rede, saidas_lineares, ativacoes_camadas, pesos_rede):
    """
    Implementa o algoritmo de backpropagation.

    Args:
        saida_desejada (numpy.ndarray): Vetor de saída esperada (n_saidas, 1).
        saida_rede (numpy.ndarray): Vetor de saída da rede neural (n_saidas, 1).
        saidas_lineares (list): Lista das saídas lineares de cada camada.
        ativacoes_camadas (list): Lista das ativações de cada camada.
        pesos_rede (list): Lista das matrizes de pesos.

    Returns:
        tuple: Uma tupla contendo os gradientes dos pesos e bias.
    """
    numero_camadas = len(ativacoes_camadas)
    gradientes_pesos = [np.zeros(w.shape) for w in pesos_rede]
    gradientes_bias = [np.zeros((pesos_rede[i].shape[0], 1)) for i in range(len(pesos_rede))] # Inicialização correta de gradientes_bias
    numero_exemplos_lote = saida_desejada.shape[1]  # m

    # Camada de saída
    erro_camada_saida = (saida_rede - saida_desejada) * derivada_tanh(saidas_lineares[-1]) # delta
    gradientes_bias[-1] = np.sum(erro_camada_saida, axis=1, keepdims=True) / numero_exemplos_lote # nabla_b
    gradientes_pesos[-1] = np.dot(erro_camada_saida, ativacoes_camadas[-2].T) / numero_exemplos_lote # nabla_w

    # Camadas ocultas
    for indice_camada in range(2, numero_camadas): # l
        saida_linear_atual = saidas_lineares[-indice_camada] # z
        derivada_tanh_atual = derivada_tanh(saida_linear_atual) # dtanh
        erro_camada_anterior = np.dot(pesos_rede[-indice_camada+1].T, erro_camada_saida) * derivada_tanh_atual # delta
        gradientes_bias[-indice_camada] = np.sum(erro_camada_anterior, axis=1, keepdims=True) / numero_exemplos_lote # nabla_b
        gradientes_pesos[-indice_camada] = np.dot(erro_camada_anterior, ativacoes_camadas[-indice_camada-1].T) / numero_exemplos_lote # nabla_w
        erro_camada_saida = erro_camada_anterior # Atualiza o erro para a próxima iteração

    return gradientes_pesos, gradientes_bias