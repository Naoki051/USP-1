import unittest
import logging
import numpy as np
from rede_neural import *
class TestNeuralNetwork(unittest.TestCase):

    def test_ativacao_range(self):
        for x in np.linspace(-10, 10, 100):
            y = ativacao(x)
            self.assertTrue(-1 <= y <= 1)
        logging.info("\033[92m[PASS] test_ativacao_range: valores de saída estão entre -1 e 1\033[0m")

    def test_derivada_ativacao_valores(self):
        for x in np.linspace(-10, 10, 100):
            d = derivada_ativacao(x)
            self.assertTrue(0 <= d <= 1)
        logging.info("\033[92m[PASS] test_derivada_ativacao_valores: derivadas estão entre 0 e 1\033[0m")

    def test_inicializacao_dos_pesos_com_bias(self):
        num_entrada, num_neuronios = 3, 2
        pesos, bias = inicializacao_dos_pesos(num_entrada, num_neuronios)
        try:
            for linha in pesos:
                for peso in linha:
                    self.assertTrue(-1 <= peso <= 1)
            for b in bias:
                self.assertTrue(-1 <= b <= 1)
            logging.info("\033[92m[PASS] test_inicializacao_dos_pesos_com_bias concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"num_entrada: {num_entrada}, num_neuronios: {num_neuronios}")
            logging.info(f"Pesos inicializados: {pesos}")
            logging.info(f"Bias inicializado: {bias}")
            logging.error(f"\033[91m[ERROR] Teste test_inicializacao_dos_pesos_com_bias falhou: {e}\033[0m")
            raise

    def test_feedforward_saida_valida(self):
        entradas = [0.5, -0.3]
        pesos, bias = inicializacao_dos_pesos(2, 2)
        _, saidas = feedforward(entradas, pesos, bias)
        for s in saidas:
            self.assertTrue(-1 <= s <= 1)
        logging.info("\033[92m[PASS] test_feedforward_saida_valida: saída está dentro do intervalo esperado\033[0m")

    def test_backpropagation_saida_valida(self):
        entradas = [1.0, 0.0]
        alvos = [1.0]
        pesos_oculta, bias_oculta = inicializacao_dos_pesos(2, 2)
        pesos_saida, bias_saida = inicializacao_dos_pesos(2, 1)

        novos_pesos_oculta, novos_bias_oculta, novos_pesos_saida, novos_bias_saida = backpropagation(
            entradas, pesos_oculta, bias_oculta, pesos_saida, bias_saida, alvos, taxa_aprendizagem=0.1
        )

        self.assertEqual(len(novos_pesos_oculta), 2)
        self.assertEqual(len(novos_bias_oculta), 2)
        self.assertEqual(len(novos_pesos_saida), 2)
        self.assertEqual(len(novos_bias_saida), 1)
        logging.info("\033[92m[PASS] test_backpropagation_saida_valida: estrutura da saída correta\033[0m")

if __name__ == "__main__":
    unittest.main()