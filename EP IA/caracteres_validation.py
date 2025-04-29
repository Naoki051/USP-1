import string
import numpy as np
from rede_mlp import treinar_mlp_validation
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

entradas = []

with open('CARACTERES COMPLETO\\X.txt', 'r') as arquivo:
    for linha in arquivo:
        elementos = [int(elemento.strip()) for elemento in linha.strip().split(',') if elemento.strip()]
        entradas.append(elementos)

tamanho_total = len(entradas)

if tamanho_total < 260:
    raise ValueError("O arquivo não contém dados suficientes para separar teste e validação.")

entradas_teste = np.array(entradas[-130:]).T
entradas_validacao = np.array(entradas[-260:-130]).T
entradas_treino = np.array(entradas[:-260]).T

saidas = []

with open('CARACTERES COMPLETO\\Y_letra.txt','r') as arquivo:
    for linha in arquivo:
        saidas.append(linha.strip())

tabela_codificacao = encode_alfabeto()

saidas_encoded = []
for letra in saidas:
    if letra in tabela_codificacao:
        saidas_encoded.append(tabela_codificacao[letra])
    else:
        print(f"Aviso: Letra '{letra}' não encontrada na tabela de codificação.")

saidas_teste = np.array(saidas_encoded[130:]).T
saidas_validacao = np.array(saidas_encoded[-260:-130]).T
saidas_treino = np.array(saidas_encoded[:-260]).T

num_entrada = entradas_treino.shape[0]
num_saida = saidas_treino.shape[0] # Deve ser 26 para one-hot encoding

parametros_treinados, custos = treinar_mlp_validation(
    entrada_treino=entradas_treino,
    saida_treino=saidas_treino,
    entrada_validacao=entradas_validacao,
    saida_validacao=saidas_validacao,
    num_entrada=num_entrada,
    num_oculta=64,
    num_saida=num_saida,
    taxa_aprendizado=0.0005,
    num_epocas=1500,
    tamanho_lote=32,
    imprimir_custo=True
)

# Plotar as curvas de custo de treinamento e validação
plt.figure(figsize=(10, 6))
plt.plot(custos['treino'], label='Custo Treino', color='blue')
plt.plot(custos['validacao'], label='Custo Validação', color='orange')
plt.xlabel('Época')
plt.ylabel('Custo')
plt.title('Curvas de Custo durante o Treinamento')
plt.legend()
plt.grid(True)
plt.show()
