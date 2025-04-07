import unittest
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def arredondar_lista(lista, casas_decimais=8):
    """Arredonda todos os elementos de uma lista para um número especificado de casas decimais."""
    return [round(elemento, casas_decimais) for elemento in lista]

def arredondar_matriz(matriz, casas_decimais=8):
    """Arredonda todos os elementos de uma matriz para um número especificado de casas decimais."""
    return [arredondar_lista(linha, casas_decimais) for linha in matriz]

from rede_neural import feedforward,ativacao

class TestFeedforward(unittest.TestCase):
    def test_feedforward(self):
        try:
            num_entrada = 2
            num_neuronios = 3
            pesos = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
            bias = [0.1, 0.2, 0.3]
            entrada = [1, 0]

            # Calcula as saídas esperadas com base na função tanh(x)
            saida_esperada = []
            for j in range(num_neuronios):
                soma = 0
                for i in range(num_entrada):
                    soma += entrada[i] * pesos[i][j]
                soma += bias[j]
                saida_esperada.append(ativacao(soma))

            somatorios_entradas, saida_calculada = feedforward(entrada, pesos, bias)

            # Arredonda as saídas para 5 casas decimais para logs
            saida_calculada_round = arredondar_lista(saida_calculada)
            saida_esperada_round = arredondar_lista(saida_esperada)

            # Usa assertAlmostEqual para comparar saídas de ponto flutuante
            self.assertAlmostEqual(saida_calculada, saida_esperada)

            logging.info("\033[92m[PASS] Teste test_feedforward concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"\tSaída calculada: {saida_calculada_round}\n\tSaída esperada: {saida_esperada_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha

    def test_feedforward_com_entrada_zero(self):
        try:
            num_entrada = 2
            num_neuronios = 3
            pesos = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
            bias = [0.1, 0.2, 0.3]
            entrada = [0, 0]

            # Calcula as saídas esperadas com base na função tanh(x)
            saida_esperada = []
            for j in range(num_neuronios):
                soma = 0
                for i in range(num_entrada):
                    soma += entrada[i] * pesos[i][j]
                soma += bias[j]
                saida_esperada.append(ativacao(soma))

            somatorios_entradas, saida_calculada = feedforward(entrada, pesos, bias)

            # Arredonda as saídas para 5 casas decimais para logs
            saida_calculada_round = arredondar_lista(saida_calculada)
            saida_esperada_round = arredondar_lista(saida_esperada)

            # Usa assertEqual para comparar saídas de ponto flutuante arredondadas
            self.assertAlmostEqual(saida_calculada, saida_esperada)

            logging.info("\033[92m[PASS] Teste test_feedforward_com_entrada_zero concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"\n\tSaída calculada: {saida_calculada_round}\n\tSaída esperada: {saida_esperada_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha


    def test_feedforward_com_pesos_e_bias_zero(self):
        try:
            pesos = [[0, 0, 0], [0, 0, 0]]
            bias = [0, 0, 0]
            entrada = [1, 1]

            saida_esperada = [0, 0, 0]
            somatorios_entradas, saida_calculada = feedforward(entrada, pesos, bias)

            # Arredonda as saídas para 5 casas decimais (se necessário)
            saida_calculada_round = arredondar_lista(saida_calculada)
            saida_esperada_round = arredondar_lista(saida_esperada)

            self.assertAlmostEqual(saida_calculada, saida_esperada)
            logging.info("\033[92m[PASS] Teste test_feedforward_com_pesos_e_bias_zero concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"\n\tSaída calculada: {saida_calculada_round}\n\tSaída esperada: {saida_esperada_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha


if __name__ == '__main__':
    unittest.main()
    