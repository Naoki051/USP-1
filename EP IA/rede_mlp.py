import numpy as np

def tanh(z):
    return np.tanh(z)

def tanh_derivada(z):
    return 1 - np.tanh(z) ** 2

# Função Sigmoide
def sigmoid(x):

    return 1 / (1 + np.exp(-x))

# Derivada da Função Sigmoide
def sigmoid_derivada(s):

    return s * (1 - s)

def inicializar_pesos(num_entrada, num_oculta, num_saida):
    """
    Inicializa os pesos para uma rede MLP com uma camada oculta.

    Args:
        num_entrada (int): Número de neurônios na camada de entrada.
        num_oculta (int): Número de neurônios na camada oculta.
        num_saida (int): Número de neurônios na camada de saída.

    Returns:
        dict: Um dicionário contendo as matrizes de pesos para cada camada.
              'W1': Pesos entre a camada de entrada e a camada oculta.
              'b1': Bias para a camada oculta.
              'W2': Pesos entre a camada oculta e a camada de saída.
              'b2': Bias para a camada de saída.
    """
    W1 = np.random.randn(num_oculta, num_entrada) * 0.01
    b1 = np.zeros((num_oculta, 1))

    W2 = np.random.randn(num_saida, num_oculta) * 0.01
    b2 = np.zeros((num_saida, 1))

    pesos = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    return pesos

# Exemplo de uso da função inicializar_pesos:
# num_entrada_exemplo = 10  # Suponha que temos 10 features de entrada
# num_oculta_exemplo = 5   # Suponha que queremos 5 neurônios na camada oculta
# num_saida_exemplo = 2    # Suponha que temos 2 neurônios na camada de saída (e.g., para classificação em 2 classes)
# 
# pesos_inicializados_exemplo = inicializar_pesos(num_entrada_exemplo, num_oculta_exemplo, num_saida_exemplo)

# print("Pesos inicializados:")
# for nome_camada, matriz in pesos_inicializados_exemplo.items():
#     print(f"\tShape de {nome_camada}: {matriz.shape}")

def feedforward_tanh(entrada, pesos):
    """
    Realiza o processo de feedforward em uma rede MLP com uma camada oculta,
    usando a função de ativação tangente hiperbólica (tanh) em ambas as camadas.

    Args:
        entrada (np.ndarray): Vetor de entrada (dimensão: num_entrada x 1).
        pesos (dict): Dicionário contendo as matrizes de pesos e bias.

    Returns:
        dict: Um dicionário contendo as saídas de cada camada (antes e depois da ativação).
              'z1': Entrada bruta da camada oculta.
              'a1': Ativação da camada oculta (usando tanh).
              'z2': Entrada bruta da camada de saída.
              'a2': Ativação da camada de saída (usando tanh).
    """
    W1 = pesos['W1']
    b1 = pesos['b1']
    W2 = pesos['W2']
    b2 = pesos['b2']

    # Camada Oculta
    z1 = np.dot(W1, entrada) + b1
    a1 = tanh(z1)  # Função de ativação Tangente Hiperbólica

    # Camada de Saída
    z2 = np.dot(W2, a1) + b2
    a2 = tanh(z2)  # Função de ativação Tangente Hiperbólica

    cache = {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2}
    return a2, cache

def feedforward_tanh(entrada, pesos):
    """Realiza o feedforward com ativação tanh."""
    W1 = pesos['W1']
    b1 = pesos['b1']
    W2 = pesos['W2']
    b2 = pesos['b2']

    z1 = np.dot(W1, entrada) + b1
    a1 = np.tanh(z1)

    z2 = np.dot(W2, a1) + b2
    a2 = np.tanh(z2)

    cache = {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2, 'entrada': entrada}
    return a2, cache

# # Exemplo de uso da função feedforward_tanh:
# # Suponha que já temos os pesos inicializados
# num_entrada_exemplo = 3
# num_oculta_exemplo = 4
# num_saida_exemplo = 1
# 
# pesos_exemplo = inicializar_pesos(num_entrada_exemplo,num_oculta_exemplo,num_saida_exemplo)
# 
# print("Pesos inicializados:")
# for nome_camada, matriz in pesos_exemplo.items():
#     print(f"\tShape de {nome_camada}: {matriz.shape}")
# 
# entrada_exemplo = np.array([[0.5, -0.1],
#                             [0.1, 0.8],
#                             [-0.2, 0.3]])  # Dimensão: (num_entrada, num_amostras)
# 
# 
# # Realizando o feedforward
# saida_rede, cache_feedforward = feedforward_tanh(entrada_exemplo, pesos_exemplo)
# 
# print("Cache do feedforward:")
# for nome_camada, valor in cache_feedforward.items():
#     print(f"  Shape de {nome_camada}: {valor.shape}")
#     
# print("Saída da rede (a2):")
# print(saida_rede)

def backward_propagation_tanh(parametros, cache, taxa_aprendizado, saida_esperada):
    """
    Realiza a backpropagation para calcular os gradientes.

    Args:
        parametros (dict): Dicionário contendo os pesos e bias.
        cache (dict): Dicionário contendo as saídas intermediárias do feedforward.
        taxa_aprendizado (float): Taxa de aprendizado
        saida_esperada (np.ndarray): Vetor da saída esperada (rótulo).

    Returns:
        dict: Um dicionário contendo os gradientes de cada parâmetro.
    """
    m = saida_esperada.shape[1]  

    a2 = cache['a2']
    a1 = cache['a1']

    entrada = cache['entrada']

    W2 = parametros['W2']

    
    dz2 = (a2 - saida_esperada)*tanh_derivada(cache['z2'])

    
    dW2 = np.dot(dz2 ,cache['z1'].T)
    
    db2 = np.sum(dz2, axis=1, keepdims=True)

    da1 = np.dot(W2.T, dz2)
    dz1 = da1 * tanh_derivada(cache['z1'])  # Derivada de tanh(z) é 1 - tanh^2(z)


    dW1 = np.dot(dz1 ,cache['entrada'].T)
    
    db1 = np.sum(dz1, axis=1, keepdims=True)

    gradientes = {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    return gradientes

def atualizar_parametros(parametros, gradientes, taxa_aprendizado):
    """
    Atualiza os parâmetros (pesos e bias) usando o gradiente descendente.

    Args:
        parametros (dict): Dicionário contendo os pesos e bias.
        gradientes (dict): Dicionário contendo os gradientes.
        taxa_aprendizado (float): A taxa de aprendizado.

    Returns:
        dict: Dicionário com os parâmetros atualizados.
    """
    parametros['W1'] = parametros['W1'] - taxa_aprendizado * gradientes['dW1']
    parametros['b1'] = parametros['b1'] - taxa_aprendizado * gradientes['db1']
    parametros['W2'] = parametros['W2'] - taxa_aprendizado * gradientes['dW2']
    parametros['b2'] = parametros['b2'] - taxa_aprendizado * gradientes['db2']

    return parametros

def treinar_mlp(entrada_treino, saida_treino, num_entrada, num_oculta, num_saida, taxa_aprendizado, num_epocas, tamanho_lote=32, imprimir_custo=False):
    """
    Realiza o treinamento da rede MLP.

    Args:
        entrada_treino (np.ndarray): Matriz de entrada de treinamento (num_entrada x num_amostras).
        saida_treino (np.ndarray): Matriz de saída de treinamento (num_saida x num_amostras).
        num_entrada (int): Número de neurônios na camada de entrada.
        num_oculta (int): Número de neurônios na camada oculta.
        num_saida (int): Número de neurônios na camada de saída.
        taxa_aprendizado (float): Taxa de aprendizado para o gradiente descendente.
        num_epocas (int): Número de épocas de treinamento.
        tamanho_lote (int): Tamanho do lote para o treinamento (padrão: 32).
        imprimir_custo (bool): Se True, imprime o custo a cada 100 épocas.

    Returns:
        dict: Os parâmetros (pesos e bias) aprendidos durante o treinamento.
        list: Uma lista dos custos ao longo das épocas.
    """
    parametros = inicializar_pesos(num_entrada, num_oculta, num_saida)
    num_amostras = entrada_treino.shape[1]
    custos = []

    for epoca in range(num_epocas):
        # Embaralhar os dados de treinamento a cada época
        permutation = np.random.permutation(num_amostras)
        entrada_embaralhada = entrada_treino[:, permutation]
        saida_embaralhada = saida_treino[:, permutation]

        num_lotes = num_amostras // tamanho_lote

        for i in range(num_lotes):
            inicio_lote = i * tamanho_lote
            fim_lote = min((i + 1) * tamanho_lote, num_amostras)

            lote_entrada = entrada_embaralhada[:, inicio_lote:fim_lote]
            lote_saida = saida_embaralhada[:, inicio_lote:fim_lote]

            # Feedforward
            saida_predita_lote, cache_lote = feedforward_tanh(lote_entrada, parametros)

            # Backpropagation
            gradientes_lote = backward_propagation_tanh(parametros, cache_lote, taxa_aprendizado, lote_saida)

            # Atualizar os parâmetros
            parametros = atualizar_parametros(parametros, gradientes_lote, taxa_aprendizado)

        # Calcular o custo ao final de cada época (usando todos os dados para ter uma métrica)
        saida_predita_total, _ = feedforward_tanh(entrada_treino, parametros)
        custo = np.mean((saida_predita_total - saida_treino)**2)
        custos.append(custo)

        if imprimir_custo and epoca % 100 == 0:
            print(f"Época {epoca}, Custo: {custo:.4f}")

    return parametros, custos

def calcular_erro(saida_predita, saida_esperada):
    """Calcula o erro quadrático médio entre a saída predita e a esperada."""
    return np.mean((saida_predita - saida_esperada)**2)

def treinar_mlp(entrada_treino, saida_treino, num_entrada, num_oculta, num_saida, taxa_aprendizado, num_epocas, imprimir_custo=False):
    """
    Realiza o treinamento de uma rede MLP.

    Args:
        entrada_treino (np.ndarray): Matriz de entrada de treinamento (num_entrada x num_amostras).
        saida_treino (np.ndarray): Matriz de saída de treinamento (num_saida x num_amostras).
        num_entrada (int): Número de neurônios na camada de entrada.
        num_oculta (int): Número de neurônios na camada oculta.
        num_saida (int): Número de neurônios na camada de saída.
        taxa_aprendizado (float): Taxa de aprendizado para o gradiente descendente.
        num_epocas (int): Número de épocas de treinamento.
        imprimir_custo (bool): Se True, imprime o custo a cada 100 épocas.

    Returns:
        dict: Parâmetros aprendidos (pesos e bias).
        list: Lista dos custos ao longo das épocas.
    """
    # Inicializar pesos e bias
    parametros = inicializar_pesos(num_entrada, num_oculta, num_saida)
    custos = []

    for epoca in range(1, num_epocas + 1):
        # Propagação para frente
        saida_predita, cache = feedforward_tanh(entrada_treino, parametros)

        # Cálculo do custo
        custo = calcular_erro(saida_predita, saida_treino)
        custos.append(custo)

        # Retropropagação
        gradientes = backward_propagation_tanh(parametros, cache, saida_treino)

        # Atualização dos parâmetros
        parametros = atualizar_parametros(parametros, gradientes, taxa_aprendizado)

        # Imprimir custo (opcional)
        if imprimir_custo and epoca % 100 == 0:
            print(f"Época {epoca}/{num_epocas}, Custo: {custo:.6f}")

    return parametros, custos

def treinar_mlp_validation(entrada_treino, saida_treino, entrada_validacao, saida_validacao, num_entrada, num_oculta, num_saida, taxa_aprendizado, num_epocas, tamanho_lote=32, imprimir_custo=False):
    """
    Realiza o treinamento da rede MLP com validação.

    Args:
        entrada_treino (np.ndarray): Matriz de entrada de treinamento (num_entrada x num_amostras_treino).
        saida_treino (np.ndarray): Matriz de saída de treinamento (num_saida x num_amostras_treino).
        entrada_validacao (np.ndarray): Matriz de entrada de validação (num_entrada x num_amostras_validacao).
        saida_validacao (np.ndarray): Matriz de saída de validação (num_saida x num_amostras_validacao).
        num_entrada (int): Número de neurônios na camada de entrada.
        num_oculta (int): Número de neurônios na camada oculta.
        num_saida (int): Número de neurônios na camada de saída.
        taxa_aprendizado (float): Taxa de aprendizado para o gradiente descendente.
        num_epocas (int): Número de épocas de treinamento.
        tamanho_lote (int): Tamanho do lote para o treinamento (padrão: 32).
        imprimir_custo (bool): Se True, imprime o custo de treinamento e validação a cada 100 épocas.

    Returns:
        dict: Os parâmetros (pesos e bias) aprendidos durante o treinamento.
        dict: Um dicionário contendo as listas de custos de treinamento e validação ao longo das épocas.
    """
    parametros = inicializar_pesos(num_entrada, num_oculta, num_saida)
    num_amostras_treino = entrada_treino.shape[1]
    custos_treino = []
    custos_validacao = []

    for epoca in range(num_epocas):
        # Embaralhar os dados de treinamento a cada época
        permutation = np.random.permutation(num_amostras_treino)
        entrada_embaralhada = entrada_treino[:, permutation]
        saida_embaralhada = saida_treino[:, permutation]

        num_lotes = num_amostras_treino // tamanho_lote

        for i in range(num_lotes):
            inicio_lote = i * tamanho_lote
            fim_lote = min((i + 1) * tamanho_lote, num_amostras_treino)

            lote_entrada = entrada_embaralhada[:, inicio_lote:fim_lote]
            lote_saida = saida_embaralhada[:, inicio_lote:fim_lote]

            # Feedforward
            saida_predita_lote, cache_lote = feedforward_tanh(lote_entrada, parametros)

            # Backpropagation
            gradientes_lote = backward_propagation_tanh(parametros, cache_lote, taxa_aprendizado, lote_saida)

            # Atualizar os parâmetros
            parametros = atualizar_parametros(parametros, gradientes_lote, taxa_aprendizado)

        # Calcular o custo de treinamento ao final de cada época
        saida_predita_treino, _ = feedforward_tanh(entrada_treino, parametros)
        custo_treino = np.mean((saida_predita_treino - saida_treino)**2)
        custos_treino.append(custo_treino)

        # Calcular o custo de validação ao final de cada época
        saida_predita_validacao, _ = feedforward_tanh(entrada_validacao, parametros)
        custo_validacao = np.mean((saida_predita_validacao - saida_validacao)**2)
        custos_validacao.append(custo_validacao)

        if imprimir_custo and epoca % 100 == 0:
            print(f"Época {epoca}, Custo Treino: {custo_treino:.4f}, Custo Validação: {custo_validacao:.4f}")

    return parametros, {'treino': custos_treino, 'validacao': custos_validacao}

def treinar_mlp_momentum(entrada_treino, saida_treino, num_entrada, num_oculta, num_saida, taxa_aprendizado, num_epocas, momento=0.9, imprimir_custo=False):
    """
    Realiza o treinamento de uma rede MLP com momento de inércia.

    Args:
        entrada_treino (np.ndarray): Matriz de entrada de treinamento (num_entrada x num_amostras).
        saida_treino (np.ndarray): Matriz de saída de treinamento (num_saida x num_amostras).
        num_entrada (int): Número de neurônios na camada de entrada.
        num_oculta (int): Número de neurônios na camada oculta.
        num_saida (int): Número de neurônios na camada de saída.
        taxa_aprendizado (float): Taxa de aprendizado para o gradiente descendente.
        num_epocas (int): Número de épocas de treinamento.
        momento (float): Fator de momento de inércia (padrão 0.9).
        imprimir_custo (bool): Se True, imprime o custo a cada 100 épocas.

    Returns:
        dict: Parâmetros aprendidos (pesos e bias).
        list: Lista dos custos ao longo das épocas.
    """
    # Inicializar pesos e bias
    parametros = inicializar_pesos(num_entrada, num_oculta, num_saida)
    custos = []

    # Inicializar velocidades para momento (começam com zeros)
    velocidades = {
        "dW1": np.zeros_like(parametros["W1"]),
        "db1": np.zeros_like(parametros["b1"]),
        "dW2": np.zeros_like(parametros["W2"]),
        "db2": np.zeros_like(parametros["b2"]),
    }

    for epoca in range(1, num_epocas + 1):
        # Propagação para frente
        saida_predita, cache = feedforward_tanh(entrada_treino, parametros)

        # Cálculo do custo
        custo = calcular_erro(saida_predita, saida_treino)
        custos.append(custo)

        # Retropropagação
        gradientes = backward_propagation_tanh(parametros, cache, saida_treino)

        # Atualizar parâmetros com momento de inércia
        for chave in parametros.keys():
            velocidades["d" + chave] = momento * velocidades["d" + chave] - taxa_aprendizado * gradientes["d" + chave]
            parametros[chave] += velocidades["d" + chave]

        # Imprimir custo (opcional)
        if imprimir_custo and epoca % 100 == 0:
            print(f"Época {epoca}/{num_epocas}, Custo: {custo:.6f}")

    return parametros, custos
