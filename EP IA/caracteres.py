import string
import numpy as np
from rede_mlp import treinar_mlp,feedforward_tanh,inicializar_pesos,backward_propagation_tanh
import matplotlib.pyplot as plt

def encode_alfabeto():
    alfabeto = string.ascii_uppercase
    tabela_encode = {}
    tamanho_encode = len(alfabeto)
    for i, letra in enumerate(alfabeto):
        vetor = [0] * tamanho_encode
        vetor[i] = 1
        tabela_encode[letra] = vetor
    return tabela_encode

saidas = []
entradas = []
with open('CARACTERES COMPLETO\\X.txt', 'r') as arquivo:
    for linha in arquivo:
        elementos = [int(elemento.strip()) for elemento in linha.strip().split(',') if elemento.strip()]
        entradas.append(elementos)

tamanho_total = len(entradas)

if tamanho_total < 260:
    raise ValueError("O arquivo não contém dados suficientes para separar 130 amostras para teste e 130 para validação.")

# Separar os últimos 130 para teste
entradas_teste = entradas[-130:]

# Separar os 130 penúltimos para validação
entradas_validacao = entradas[-260:-130]

# O restante dos dados será para treinamento
entradas_treino = entradas[:-260]

print(f"Tamanho do conjunto de treino: {len(entradas_treino)}")
print(f"Tamanho do conjunto de validação: {len(entradas_validacao)}")
print(f"Tamanho do conjunto de teste: {len(entradas_teste)}")

# Você pode agora usar entradas_treino, entradas_validacao e entradas_teste
with open('CARACTERES COMPLETO\Y_letra.txt','r') as arquivo:
    for linha in arquivo:
        saidas.append(linha.strip())

tabela_codificacao = encode_alfabeto()
for item in tabela_codificacao:
    print(item,tabela_codificacao[item])
print(entradas[0])
print(saidas[0])

entradas = np.array(entradas).T

saidas_encoded = []
for letra in saidas:
    if letra in tabela_codificacao:
        saidas_encoded.append(tabela_codificacao[letra])
    else:
        print(f"Aviso: Letra '{letra}' não encontrada na tabela de codificação.")
saidas = np.array(saidas_encoded).T

parametros_treinados, custos =treinar_mlp(
    entrada_treino= entradas,
    saida_treino= saidas,
    num_entrada=120,
    num_oculta=64,
    num_saida=26,
    taxa_aprendizado=0.1,
    num_epocas=5000,
    imprimir_custo=True,
)

# Plotar a curva de custo
plt.figure(figsize=(8, 5))
plt.plot(custos, color='blue')
plt.xlabel('Época')
plt.ylabel('Custo')
plt.title('Curva de Custo durante o Treinamento')
plt.grid(True)
plt.show()