import unittest
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def arredondar_lista(lista, casas_decimais=5):
    """Arredonda todos os elementos de uma lista para um número especificado de casas decimais."""
    return [round(elemento, casas_decimais) for elemento in lista]

def arredondar_matriz(matriz, casas_decimais=5):
    """Arredonda todos os elementos de uma matriz para um número especificado de casas decimais."""
    return [arredondar_lista(linha, casas_decimais) for linha in matriz]

from rede_neural import inicializacao_dos_pesos

class TestInicializacaoPesos(unittest.TestCase):
    def test_inicializacao_dos_pesos_com_bias(self):
        try:
            num_entrada = 2
            num_neuronios = 3
            pesos, bias = inicializacao_dos_pesos(num_entrada, num_neuronios)

            pesos_round = arredondar_matriz(pesos)
            bias_round = arredondar_lista(bias)
            # Verifica se pesos e bias têm as dimensões corretas
            self.assertEqual(len(pesos), num_entrada)
            self.assertEqual(len(pesos[0]), num_neuronios)
            self.assertEqual(len(bias), num_neuronios)

            # Verifica se os valores estão dentro da faixa esperada
            for i in range(num_entrada):
                for j in range(num_neuronios):
                    self.assertTrue(-0.01 <= pesos[i][j] <= 0.01)

            for b in bias:
                self.assertTrue(-0.01 <= b <= 0.01)

            logging.info("\033[92m[PASS] Teste test_inicializacao_dos_pesos_com_bias concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"num_entrada: {num_entrada}, num_neuronios: {num_neuronios}")
            logging.info(f"Pesos inicializados: {pesos_round}")
            logging.info(f"Bias inicializado: {bias_round}")
            logging.error(f"\033[91m[ERROR] Teste test_inicializacao_dos_pesos_com_bias falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha

    def test_inicializacao_dos_pesos_sem_bias(self):
        try:
            num_entrada = 2
            num_neuronios = 3
            pesos, bias = inicializacao_dos_pesos(num_entrada, num_neuronios, use_bias=False)

            pesos_round = arredondar_matriz(pesos)
            bias_round = arredondar_lista(bias)

            # Verifica se pesos e bias têm as dimensões corretas
            self.assertEqual(len(pesos), num_entrada)
            self.assertEqual(len(pesos[0]), num_neuronios)
            self.assertEqual(len(bias), num_neuronios)

            # Verifica se os valores estão dentro da faixa esperada para pesos
            for i in range(num_entrada):
                for j in range(num_neuronios):
                    self.assertTrue(-0.01 <= pesos[i][j] <= 0.01)

            # Verifica se o bias é zero
            for b in bias:
                self.assertEqual(b, 0)
            logging.info("\033[92m[PASS] Teste test_inicializacao_dos_pesos_sem_bias concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"num_entrada: {num_entrada}, num_neuronios: {num_neuronios}")
            logging.info(f"Pesos inicializados: {pesos_round}")
            logging.info(f"Bias inicializado: {bias_round}")
            logging.error(f"\033[91m[ERROR] Teste test_inicializacao_dos_pesos_sem_bias falhou: {e}\033[0m")

            raise  # Re-lança a exceção para que o unittest reporte a falha

if __name__ == '__main__':   
    unittest.main()
