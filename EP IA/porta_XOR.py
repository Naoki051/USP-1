from rede_mlp import treinar_mlp_momentum, feedforward_tanh
import numpy as np
import matplotlib.pyplot as plt

# Exemplo de uso da função de treinamento
if __name__ == "__main__":
    # Definir a arquitetura da rede e hiperparâmetros
    num_entrada = 2
    num_oculta = 3
    num_saida = 1
    taxa_aprendizado = 0.009
    num_epocas = 4000

    # Criar um conjunto de dados de treinamento simples (problema XOR como regressão)
    entrada_treino_xor = np.array([
        [0, 0, 1, 1],
        [0, 1, 0, 1]
    ])
    saida_treino_xor = np.array([
        [0, 1, 1, 0]
    ])

    # Treinar a rede MLP
    parametros_aprendidos_xor, custos_xor = treinar_mlp_momentum(
        entrada_treino_xor, 
        saida_treino_xor, 
        num_entrada, 
        num_oculta, 
        num_saida, 
        taxa_aprendizado, 
        num_epocas,
        momento=0.99,
        imprimir_custo=True
    )

    # Plotar a curva de custo
    plt.figure(figsize=(8, 5))
    plt.plot(custos_xor, color='blue')
    plt.xlabel('Época')
    plt.ylabel('Custo')
    plt.title('Curva de Custo durante o Treinamento (XOR como Regressão)')
    plt.grid(True)
    plt.show()

    # Função para prever novos exemplos
    def prever(entrada, parametros):
        saida, _ = feedforward_tanh(entrada, parametros)
        return saida

    # Fazer previsões com os parâmetros aprendidos
    print("\nPrevisões após o treinamento (XOR como Regressão):")
    for i in range(entrada_treino_xor.shape[1]):
        entrada_teste = entrada_treino_xor[:, i].reshape(-1, 1)  # Usar -1 para manter flexível
        previsao = prever(entrada_teste, parametros_aprendidos_xor)
        print(f"Entrada: [{entrada_teste[0, 0]}, {entrada_teste[1, 0]}], Previsão: {previsao[0, 0]:.4f}")
    print(entrada_treino_xor.shape)
    print(saida_treino_xor.shape)