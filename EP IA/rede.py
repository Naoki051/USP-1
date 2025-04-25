import numpy as np

def inicializar_parametros(camadas):
  """
  Inicializa os pesos e bias para uma rede neural MLP.

  Args:
    camadas: Uma lista de inteiros representando o número de neurônios em cada camada,
             incluindo a camada de entrada.

  Returns:
    Um dicionário contendo os pesos 'W' e bias 'b' para cada camada.
    As chaves do dicionário são 'W1', 'b1', 'W2', 'b2', etc.
  """
  parametros = {}
  num_camadas = len(camadas)
  for l in range(1, num_camadas):
    parametros['W' + str(l)] = np.random.randn(camadas[l], camadas[l-1]) * 0.01
    parametros['b' + str(l)] = np.zeros((camadas[l], 1))
  return parametros

def inicializar_parametros_e_bias(camadas):
  """
  Inicializa os pesos e bias para uma rede neural MLP.

  Args:
    camadas: Uma lista de inteiros representando o número de neurônios em cada camada,
             incluindo a camada de entrada.

  Returns:
    Um dicionário contendo os pesos 'W' e bias 'b' para cada camada.
    As chaves do dicionário são 'W1', 'b1', 'W2', 'b2', etc.
  """
  parametros = {}
  num_camadas = len(camadas)
  for l in range(1, num_camadas):
    parametros['W' + str(l)] = np.random.randn(camadas[l], camadas[l-1]) * 0.01
    parametros['b' + str(l)] = np.random.randn(camadas[l], 1) * 0.01  # Inicializando bias com pequenos valores aleatórios e forma correta
  return parametros

# Exemplo de uso: uma rede com 3 camadas (2 neurônios na entrada, 4 na oculta, 1 na saída)
# estrutura_camadas = [2, 4, 1]
# parametros_inicializados = inicializar_parametros_e_bias(estrutura_camadas)
# for item in parametros_inicializados:
#   print(item,":\n",parametros_inicializados[item])

import numpy as np

def f_ativacao(Z):
  """
  Função de ativação tangente hiperbólica.

  Args:
    Z: A entrada para a função tanh.

  Returns:
    A saída da função tanh.
  """
  A = np.tanh(Z)
  return A

def f_ativacao_derivada(A):
  """
  Calcula a derivada da função tangente hiperbólica.

  Args:
    A: A saída da função tanh (f_ativacao(Z)).

  Returns:
    A derivada da função tanh em relação a Z.
  """
  derivada = 1 - np.power(A, 2)
  return derivada

def feedforward(X, parametros):
  """
  Implementa a propagação para frente através da rede neural usando a função tanh.

  Args:
    X: A matriz de dados de entrada Matriz(n_amostras, n_caracteristicas).
    parametros: Um dicionário contendo os pesos 'W' e bias 'b' de cada camada.

  Returns:
    Um dicionário contendo as saídas de cada camada (incluindo a entrada),
    armazenadas com as chaves 'A0', 'A1', 'A2', etc., e os valores de 'Z'
    para cada camada, armazenados com as chaves 'Z1', 'Z2', etc.
  """
  memoria_cache = {"A0": X}
  num_camadas = len(parametros) // 2

  for l in range(1, num_camadas + 1):
    W = parametros['W' + str(l)]
    b = parametros['b' + str(l)]

    A_prev = memoria_cache['A' + str(l - 1)]

    somatorio_entrada = np.dot(W, A_prev) + b
    resultado = f_ativacao(somatorio_entrada)  # Usando a função tanh aqui
    memoria_cache['Z' + str(l)] = somatorio_entrada
    memoria_cache['A' + str(l)] = resultado

  return memoria_cache

# Exemplo de uso (continuando do exemplo anterior):
# estrutura_camadas = [2, 4, 1]
# parametros_inicializados = inicializar_parametros(estrutura_camadas)

# for item in parametros_inicializados:
#   print(item,":\n",parametros_inicializados[item])
# print("---"*20)

# entradas_exemplo = np.array([[0.5, 0.1],
#                       [0.8, 0.3],
#                       [0.2, 0.9],
#                       [0.4, 0.1]]).T

# saidas_feedforward_tanh = feedforward(entradas_exemplo, parametros_inicializados)

# print("\nSaídas do Feedforward (usando tanh):")
# for item in saidas_feedforward_tanh:
#   print(item,":\n",saidas_feedforward_tanh[item])

# Demonstração da derivada da tanh para um valor de saída de exemplo
# A_exemplo_tanh = saidas_feedforward_tanh['A1']
# derivada_tanh_exemplo = f_ativacao_derivada(A_exemplo_tanh)
# print("\nDerivada da tanh para a saída da primeira camada:")
# print(derivada_tanh_exemplo)

import numpy as np

def calcular_custo_mse(saida_camada_saida, alvos):
  """
  Calcula o custo do erro quadrático médio (MSE).

  Args:
    saida_camada_saida: A saída da camada final da rede (a predição).
    alvos: Os rótulos verdadeiros correspondentes.

  Returns:
    O valor do custo MSE.
  """
  m = alvos.shape[1]  # Número de amostras
  custo = np.sum(np.power(saida_camada_saida - alvos, 2)) / (2 * m)
  return custo

def backpropagation(parametros, memoria_cache, Y):
  """
  Implementa a retropropagação para calcular os gradientes.

  Args:
    parametros: Um dicionário contendo os pesos 'W' e bias 'b'.
    memoria_cache: Um dicionário contendo as saídas de cada camada ('A's) e os valores 'Z's.
    X: A matriz de dados de entrada.
    Y: Os rótulos verdadeiros correspondentes.

  Returns:
    Um dicionário contendo os gradientes dos pesos 'dW' e bias 'db' para cada camada.
  """
  gradientes = {}
  num_camadas = len(parametros) // 2
  m = Y.shape[1]  # Número de amostras

  # Camada de saída (última camada)
  AL = memoria_cache['A' + str(num_camadas)]
  dZL = AL - Y
  gradientes['dW' + str(num_camadas)] = np.dot(dZL, memoria_cache['A' + str(num_camadas - 1)].T) / m
  # db[L] = np.mean(dZL, axis=1, keepdims=True)
  gradientes['db' + str(num_camadas)] = np.mean(dZL, axis=1, keepdims=True)
  dA_prev = np.dot(parametros['W' + str(num_camadas)].T, dZL)

  # Camadas ocultas (da camada num_camadas-1 até a camada 1)
  for l in reversed(range(1, num_camadas)):
    A_atual = memoria_cache['A' + str(l)]
    dZ = dA_prev * f_ativacao_derivada(A_atual)
    gradientes['dW' + str(l)] = np.dot(dZ, memoria_cache['A' + str(l - 1)].T) / m
    gradientes['db' + str(l)] = np.sum(dZ, axis=1, keepdims=True) / m
    if l > 1:
      dA_prev = np.dot(parametros['W' + str(l)].T, dZ)

  return gradientes
  
def atualizar_parametros(parametros, gradientes, taxa_aprendizado):
  num_camadas = len(parametros) // 2
  for l in range(1, num_camadas + 1):
    parametros['W' + str(l)] = parametros['W' + str(l)] - taxa_aprendizado * gradientes['dW' + str(l)]
    parametros['b' + str(l)] = parametros['b' + str(l)] - taxa_aprendizado * gradientes['db' + str(l)]
  return parametros


def treinar_mlp(camadas, X, Y, num_epocas, taxa_aprendizado, print_custo=False):
  parametros = inicializar_parametros_e_bias(camadas)
  custos = []

  for i in range(num_epocas):
    memoria_cache = feedforward(X, parametros)
    AL = memoria_cache['A' + str(len(camadas) - 1)]
    custo = calcular_custo_mse(AL, Y)
    custos.append(custo)
    gradientes = backpropagation(parametros, memoria_cache, Y)
    parametros = atualizar_parametros(parametros, gradientes, taxa_aprendizado)

  return parametros, custos

def treinar_mlp_com_parada_antecipada(camadas, X_treino, Y_treino, X_val, Y_val, num_epocas, taxa_aprendizado, paciencia=10, print_custo=False):
    parametros = inicializar_parametros_e_bias(camadas)
    custos_treino = []
    custos_val = []
    melhores_parametros = parametros.copy()
    melhor_custo_val = float('inf')
    epocas_sem_melhora = 0

    for i in range(num_epocas):
        # Treinamento
        memoria_cache_treino = feedforward(X_treino, parametros)
        AL_treino = memoria_cache_treino['A' + str(len(camadas) - 1)]
        custo_treino = calcular_custo_mse(AL_treino, Y_treino)
        custos_treino.append(custo_treino)
        gradientes = backpropagation(parametros, memoria_cache_treino, Y_treino)
        parametros = atualizar_parametros(parametros, gradientes, taxa_aprendizado)

        # Validação
        memoria_cache_val = feedforward(X_val, parametros)
        AL_val = memoria_cache_val['A' + str(len(camadas) - 1)]
        custo_val = calcular_custo_mse(AL_val, Y_val)
        custos_val.append(custo_val)

        if custo_val < melhor_custo_val:
            melhor_custo_val = custo_val
            melhores_parametros = parametros.copy()
            epocas_sem_melhora = 0
        else:
            epocas_sem_melhora += 1
            if epocas_sem_melhora >= paciencia:
                print(f"Parada antecipada acionada na época {i+1}.")
                break

        if print_custo and i % 100 == 0:
            print(f"Época {i}: Custo treino = {custo_treino:.4f}, Custo val = {custo_val:.4f}")

    return melhores_parametros, custos_treino, custos_val