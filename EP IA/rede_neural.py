import numpy as np

def f_ativacao(z):
    """
    Implementa a função sigmoide.

    Args:
        z (numpy.ndarray): A entrada da função sigmoide.

    Returns:
        numpy.ndarray: A saída da função sigmoide.
    """
    return 1 / (1 + np.exp(-z))

def f_derivada(dA):
    """
    Calcula a derivada da função sigmoide.

    Args:
        dA (numpy.ndarray): A saída da função sigmoide.

    Returns:
        numpy.ndarray: A derivada da função sigmoide correspondente à entrada dA.
    """
    s = 1 / (1 + np.exp(-dA))
    return s * (1 - s)

def inicializar_parametros(n_entrada, n_escondida, n_saida):
    """
    Inicializa os pesos e bias para uma rede neural MLP com uma camada escondida.

    Args:
        n_entrada (int): Número de neurônios na camada de entrada.
        n_escondida (int): Número de neurônios na camada escondida.
        n_saida (int): Número de neurônios na camada de saída.

    Returns:
        dict: Um dicionário contendo os pesos (W1, W2) e bias (b1, b2) inicializados.
              - W1: pesos da camada de entrada para a camada escondida (matriz de dimensões n_escondida x n_entrada).
              - b1: bias da camada escondida (vetor de dimensões n_escondida x 1).
              - W2: pesos da camada escondida para a camada de saída (matriz de dimensões n_saida x n_escondida).
              - b2: bias da camada de saída (vetor de dimensões n_saida x 1).
    """
    # Inicializando os pesos com valores aleatórios pequenos (distribuição normal)
    W1 = np.random.randn(n_escondida, n_entrada) * 0.01
    W2 = np.random.randn(n_saida, n_escondida) * 0.01

    # Inicializando os bias com zeros
    b1 = np.zeros((n_escondida, 1))
    b2 = np.zeros((n_saida, 1))

    parametros = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    return parametros

def feedfoward(X, parametros):
    """
    Implementa a propagação para frente em uma rede neural MLP com uma camada escondida.

    Args:
        X (numpy.ndarray): Dados de entrada (matriz de dimensões n_entrada x m, onde m é o número de exemplos).
        parametros (dict): Dicionário contendo os pesos (W1, W2) e bias (b1, b2).

    Returns:
        dict: Um dicionário contendo as saídas de cada camada (Z1, A1, Z2, A2) da última propagação.
              - Z1: saída linear da camada escondida (W1 * X + b1).
              - A1: saída da função de ativação da camada escondida (sigmoid(Z1)).
              - Z2: saída linear da camada de saída (W2 * A1 + b2).
              - A2: saída da função de ativação da camada de saída (sigmoid(Z2)).
    """
    # Recupera os parâmetros do dicionário
    W1 = parametros['W1']
    b1 = parametros['b1']
    W2 = parametros['W2']
    b2 = parametros['b2']

    # Camada escondida 
    # Z1 = [W1 x X] multiplicação de matrizes - representa o somatório de entrada 
    # A1 = aplicação da função de ativação em Z1 - saída da camada oculta 
    Z1 = np.dot(W1, X) + b1
    A1 = f_ativacao(Z1)

    # Camada de saída
    # Z2 = [W2 x A1] multiplicação de matrizes 
    # A1 = aplicação da função de ativação em Z2 
    Z2 = np.dot(W2, A1) + b2
    A2 = f_ativacao(Z2)

    # Dados das entradas (somatórios) e saídas de cada camada para retropropagacao_mse
    cache = {'Z1': Z1, 'A1': A1, 'Z2': Z2, 'A2': A2}
    return A2, cache

def calcular_custo_mse(A2, Y):
    """
    Calcula o custo do Erro Quadrático Médio (MSE).

    Args:
        A2 (numpy.ndarray): A saída da camada de saída (previsões).
                             Dimensões: (n_saida x número de exemplos).
        Y (numpy.ndarray): Os valores verdadeiros.
                          Dimensões: (n_saida x número de exemplos).

    Returns:
        float: O valor do custo MSE.
    """
    m = Y.shape[1]  # Quantidade de elemetos
    # MSE = (1/m) * sum((A2 - Y)^2)
    custo = (1/m) * np.sum((A2 - Y)**2)
    return custo

def retropropagacao_mse(parametros, cache, X, Y):
    """
    Implementa a retropropagação para calcular os gradientes.

    Args:
        parametros (dict): Dicionário contendo os pesos (W1, W2) e bias (b1, b2).
        cache (dict): Dicionário contendo as saídas de cada camada (Z1, A1, Z2, A2).
        X (numpy.ndarray): Dados de entrada.
        Y (numpy.ndarray): Rótulos verdadeiros.

    Returns:
        dict: Um dicionário contendo os gradientes com relação aos pesos e bias (dW1, db1, dW2, db2).
    """
    m = X.shape[1]

    # Recupera W1, W2 do dicionário de parâmetros
    W1 = parametros['W1']
    W2 = parametros['W2']

    # Recupera A1, A2, Z1 do dicionário de cache
    A1 = cache['A1']
    A2 = cache['A2']
    Z1 = cache['Z1']

    # Gradiente da função de custo com relação a A2
    # Fórmula da derivada do MSE com relação a A2: dJ/dA2 = 2 * (A2 - Y) / m
    dA2 = 2 * (A2 - Y) / m
    # Gradiente da função de custo com relação a Z2 (ativação linear: d(Z2)/d(Z2) = 1)
    # Fórmula: dJ/dZ2 = dJ/dA2 * dA2/dZ2 = dA2 * 1 = dA2
    dZ2 = dA2
    # Gradiente da função de custo com relação a W2
    # Fórmula: dJ/dW2 = dJ/dZ2 * dZ2/dW2 = dZ2 . A1^T
    dW2 = np.dot(dZ2, A1.T)
    # Gradiente da função de custo com relação a b2
    # Fórmula: dJ/db2 = dJ/dZ2 * dZ2/db2 = sum(dZ2, axis=1, keepdims=True)
    db2 = np.sum(dZ2, axis=1, keepdims=True)
    # Gradiente da função de custo com relação a A1
    # Fórmula: dJ/dA1 = dJ/dZ2 * dZ2/dA1 = W2^T . dZ2
    dA1 = np.dot(W2.T, dZ2)
    # Gradiente da função de custo com relação a Z1 (ativação sigmoide: dA1/dZ1 = sigmoid_derivada(Z1))
    # Fórmula: dJ/dZ1 = dJ/dA1 * dA1/dZ1 = dA1 * sigmoid_derivada(Z1)
    dZ1 = dA1 * f_derivada(Z1)
    # Gradiente da função de custo com relação a W1
    # Fórmula: dJ/dW1 = dJ/dZ1 * dZ1/dW1 = dZ1 . X^T
    dW1 = np.dot(dZ1, X.T)
    # Gradiente da função de custo com relação a b1
    # Fórmula: dJ/db1 = dJ/dZ1 * dZ1/db1 = sum(dZ1, axis=1, keepdims=True)
    db1 = np.sum(dZ1, axis=1, keepdims=True)

    gradientes = {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    return gradientes

def calcular_custo_mae(A2, Y):
    """
    Calcula o custo do Erro Absoluto Médio (MAE).

    Args:
        A2 (numpy.ndarray): A saída da camada de saída (previsões).
                             Dimensões: (n_saida x número de exemplos).
        Y (numpy.ndarray): Os valores verdadeiros.
                          Dimensões: (n_saida x número de exemplos).

    Returns:
        float: O valor do custo MAE.
        Fórmula: MAE = (1/m) * sum(|A2 - Y|)
    """
    m = Y.shape[1]  # Número de exemplos
    custo = (1/m) * np.sum(np.abs(A2 - Y))
    return custo

def retropropagacao_mae(parametros, cache, X, Y):
    """
    Implementa a retropropagação para calcular os gradientes usando o custo MAE.

    Args:
        parametros (dict): Dicionário contendo os pesos (W1, W2) e bias (b1, b2).
        cache (dict): Dicionário contendo as saídas de cada camada (Z1, A1, Z2, A2).
        X (numpy.ndarray): Dados de entrada.
        Y (numpy.ndarray): Rótulos verdadeiros.

    Returns:
        dict: Um dicionário contendo os gradientes com relação aos pesos e bias (dW1, db1, dW2, db2).
    """
    m = X.shape[1]

    # Recupera W1, W2 do dicionário de parâmetros
    W1 = parametros['W1']
    W2 = parametros['W2']

    # Recupera A1, A2, Z1 do dicionário de cache
    A1 = cache['A1']
    A2 = cache['A2']
    Z1 = cache['Z1']

    # Gradiente da função de custo com relação a A2
    # Fórmula da derivada do MAE com relação a A2: dJ/dA2 = (1/m) * sgn(A2 - Y)
    dA2 = np.sign(A2 - Y) / m

    # Gradiente da função de custo com relação a Z2 (ativação linear: d(Z2)/d(Z2) = 1)
    # Fórmula: dJ/dZ2 = dJ/dA2 * dA2/dZ2 = dA2 * 1 = dA2
    dZ2 = dA2

    # Gradiente da função de custo com relação a W2
    # Fórmula: dJ/dW2 = dJ/dZ2 * dZ2/dW2 = dZ2 . A1^T
    dW2 = np.dot(dZ2, A1.T)
    # Gradiente da função de custo com relação a b2
    # Fórmula: dJ/db2 = dJ/dZ2 * dZ2/db2 = sum(dZ2, axis=1, keepdims=True)
    db2 = np.sum(dZ2, axis=1, keepdims=True)

    # Gradiente da função de custo com relação a A1
    # Fórmula: dJ/dA1 = dJ/dZ2 * dZ2/dA1 = W2^T . dZ2
    dA1 = np.dot(W2.T, dZ2)

    # Gradiente da função de custo com relação a Z1 (ativação sigmoide: dA1/dZ1 = sigmoid_derivada(Z1))
    # Fórmula: dJ/dZ1 = dJ/dA1 * dA1/dZ1 = dA1 * sigmoid_derivada(Z1)
    dZ1 = dA1 * f_derivada(Z1)

    # Gradiente da função de custo com relação a W1
    # Fórmula: dJ/dW1 = dJ/dZ1 * dZ1/dW1 = dZ1 . X^T
    dW1 = np.dot(dZ1, X.T)
    # Gradiente da função de custo com relação a b1
    # Fórmula: dJ/db1 = dJ/dZ1 * dZ1/db1 = sum(dZ1, axis=1, keepdims=True)
    db1 = np.sum(dZ1, axis=1, keepdims=True)

    gradientes = {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    return gradientes

def atualizar_parametros(parametros, gradientes, taxa_de_aprendizado):
    """
    Atualiza os parâmetros da rede neural usando o gradiente descendente.

    Args:
        parametros (dict): Dicionário contendo os pesos (W1, W2) e bias (b1, b2).
        gradientes (dict): Dicionário contendo os gradientes (dW1, db1, dW2, db2).
        taxa_de_aprendizado (float): A taxa de aprendizado (alpha) para o gradiente descendente.

    Returns:
        dict: Um dicionário contendo os parâmetros atualizados (W1, b1, W2, b2).
    """
    # Recupera os parâmetros
    W1 = parametros['W1']
    b1 = parametros['b1']
    W2 = parametros['W2']
    b2 = parametros['b2']

    # Recupera os gradientes
    dW1 = gradientes['dW1']
    db1 = gradientes['db1']
    dW2 = gradientes['dW2']
    db2 = gradientes['db2']

    # Atualiza os parâmetros usando a regra do gradiente descendente:
    # W = W - alpha * dW
    # b = b - alpha * db

    W1 = W1 - taxa_de_aprendizado * dW1
    b1 = b1 - taxa_de_aprendizado * db1
    W2 = W2 - taxa_de_aprendizado * dW2
    b2 = b2 - taxa_de_aprendizado * db2

    # Atualiza o dicionário de parâmetros
    parametros_atualizados = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    return parametros_atualizados

def prever(X, parametros):
    """
    Realiza a previsão usando os parâmetros aprendidos.

    Args:
        X (numpy.ndarray): Dados de entrada (n_entrada x m).
        parametros (dict): Dicionário contendo os parâmetros aprendidos.

    Returns:
        numpy.ndarray: As previsões (0 ou 1) para cada exemplo.
    """
    A2, cache = feedfoward(X, parametros)
    previsoes = (A2 > 0.5).astype(int) # Para o caso da porta XOR
    return previsoes

def treinar_mlp_mae(X, Y, n_escondida, taxa_de_aprendizado, n_iteracoes):
    n_entrada = X.shape[0]
    n_saida = Y.shape[0]
    m = Y.shape[1]

    parametros = inicializar_parametros(n_entrada, n_escondida, n_saida)
    custos = []

    for i in range(n_iteracoes):
        A2, cache = feedfoward(X, parametros) # Usando saída linear para regressão
        custo = calcular_custo_mae(A2, Y)
        custos.append(custo)
        gradientes = retropropagacao_mae(parametros, cache, X, Y)
        parametros = atualizar_parametros(parametros, gradientes, taxa_de_aprendizado)

        if i % 500 == 0:
            print(f"Custo MAE após a iteração {i}: {custo}")
    return parametros, custos

def treinar_mlp_mse(X, Y, n_escondida, taxa_de_aprendizado, n_iteracoes):
    """
    Treina uma rede neural MLP com uma camada escondida usando gradiente descendente.

    Args:
        X (numpy.ndarray): Dados de entrada (n_entrada x m).
        Y (numpy.ndarray): Rótulos verdadeiros (n_saida x m).
        n_escondida (int): Número de neurônios na camada escondida.
        taxa_de_aprendizado (float): A taxa de aprendizado para o gradiente descendente.
        n_iteracoes (int): Número de iterações de treinamento.

    Returns:
        dict: Um dicionário contendo os parâmetros aprendidos (W1, b1, W2, b2).
        list: Uma lista dos custos calculados em cada iteração.
    """
    n_entrada = X.shape[0]
    n_saida = Y.shape[0]
    m = Y.shape[1]  # Número de exemplos

    # Inicializa os parâmetros
    parametros = inicializar_parametros(n_entrada, n_escondida, n_saida)
    custos = []

    # Loop de treinamento
    for i in range(n_iteracoes):
        # Propagação para frente
        A2, cache = feedfoward(X, parametros)

        # Cálculo do custo (usando entropia cruzada para classificação binária)
        custo = calcular_custo_mse(A2, Y)
        custos.append(custo)

        # Retropropagação
        gradientes = retropropagacao_mse(parametros, cache, X, Y)

        # Atualização dos parâmetros
        parametros = atualizar_parametros(parametros, gradientes, taxa_de_aprendizado)

        # Imprime o custo a cada 100 iterações
        if i % 100 == 0:
            print(f"Custo após a iteração {i}: {custo}")

    return parametros, custos

def calcular_acuracia(previsoes, rotulos):
    """
    Calcula a acurácia das previsões em relação aos rótulos verdadeiros.

    Args:
        previsoes (numpy.ndarray): As previsões do modelo (formato dependente do problema,
                                    geralmente 0 ou 1 para classificação binária).
        rotulos (numpy.ndarray): Os rótulos verdadeiros correspondentes.

    Returns:
        float: A acurácia (proporção de previsões corretas).
    """
    if previsoes.shape != rotulos.shape:
        raise ValueError("As dimensões das previsões e dos rótulos devem ser as mesmas.")

    comparacao = (previsoes == rotulos)
    acuracia = np.mean(comparacao)
    return acuracia