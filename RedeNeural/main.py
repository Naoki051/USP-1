from rede_neural import *
import matplotlib.pyplot as plt
def treinar_rede(dados, num_entrada, num_oculta, num_saida, taxa_aprendizagem, epocas):
    pesos_oculta, bias_oculta = inicializacao_dos_pesos(num_entrada, num_oculta)
    pesos_saida, bias_saida = inicializacao_dos_pesos(num_oculta, num_saida)
    erros_por_epoca = []

    for epoca in range(epocas):
        erro_total = 0
        for entrada, alvo in dados:
            pesos_oculta, bias_oculta, pesos_saida, bias_saida = backpropagation(
                entrada, pesos_oculta, bias_oculta, pesos_saida, bias_saida, alvo, taxa_aprendizagem
            )

            _, saida_rede = feedforward(
                *feedforward(entrada, pesos_oculta, bias_oculta)[1:], pesos_saida, bias_saida
            )

            erro_total += sum((s - a) ** 2 for s, a in zip(saida_rede, alvo))

        mse = erro_total / len(dados)
        erros_por_epoca.append(mse)

    # Plotando erro
    plt.figure(figsize=(8, 5))
    plt.plot(erros_por_epoca, label='Erro quadrático médio (MSE)', color='blue')
    plt.xlabel("Épocas")
    plt.ylabel("Erro")
    plt.title("Evolução do erro durante o treinamento")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return pesos_oculta, bias_oculta, pesos_saida, bias_saida, erros_por_epoca

if __name__ == "__main__":
    dados = [
    ([0, 0], [0]),
    ([0, 1], [0]),
    ([1, 0], [0]),
    ([1, 1], [1])
    ]

    pesos_oculta, bias_oculta, pesos_saida, bias_saida, erros = treinar_rede(
        dados,
        num_entrada=2,
        num_oculta=2,
        num_saida=1,
        taxa_aprendizagem=0.5,
        epocas=200
    )