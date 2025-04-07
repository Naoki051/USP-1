import unittest
import logging
import numpy as np
# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def arredondar_lista(lista, casas_decimais=5):
    """Arredonda todos os elementos de uma lista para um número especificado de casas decimais."""
    return [round(elemento, casas_decimais) for elemento in lista]

def arredondar_matriz(matriz, casas_decimais=5):
    """Arredonda todos os elementos de uma matriz para um número especificado de casas decimais."""
    return [arredondar_lista(linha, casas_decimais) for linha in matriz]

from rede_neural import inicializacao_dos_pesos, feedforward
class TestFeedforwardComInicializacao(unittest.TestCase):
    def test_feedforward_com_inicializacao(self):
        try:
            num_entrada = 2
            num_neuronios = 3
            pesos, bias = inicializacao_dos_pesos(num_entrada, num_neuronios)
            entrada = [1, 0]

            pesos_round = arredondar_matriz(pesos)
            bias_round = arredondar_lista(bias)
            
            somatorios_entradas, saida_calculada = feedforward(entrada,pesos, bias)

            saida_calculada_round = arredondar_lista(saida_calculada)
            
            # Verifica se a saída calculada tem o tamanho correto
            self.assertEqual(len(saida_calculada), num_neuronios)

            # Verifica se a saída calculada está dentro de uma faixa razoável
            for valor_saida in saida_calculada:
                self.assertTrue(-1 <= valor_saida <= 1)

            logging.info("\033[92m[PASS] Teste test_feedforward_com_inicializacao concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"\tnum_entrada: {num_entrada}, num_neuronios: {num_neuronios}")
            logging.info(f"\tPesos inicializados: {pesos_round}")
            logging.info(f"\tBias inicializado: {bias_round}")
            logging.info(f"\tEntrada: {entrada}")
            logging.info(f"\tSaída calculada: {saida_calculada_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward_com_inicializacao falhou: {e}\033[0m")
            raise
        
    def test_feedforward_com_inicializacao_dimesoes_maiores(self):
        try:
            num_entrada = 120
            num_neuronios = 30
            pesos, bias = inicializacao_dos_pesos(num_entrada, num_neuronios)
            # Cria uma entrada com 120 elementos usando um laço
            entrada = [i % 2 for i in range(num_entrada)]  # Alterna entre 0 e 1
            somatorios_entradas, saida_calculada = feedforward(entrada,pesos, bias)

            # Verifica se a saída calculada tem o tamanho correto
            self.assertEqual(len(saida_calculada), num_neuronios)

            # Verifica se a saída calculada está dentro de uma faixa razoável
            saida_calculada_round = arredondar_lista(saida_calculada[:5])
            for valor_saida in saida_calculada:
                self.assertTrue(-1 <= valor_saida <= 1)

            logging.info("\033[92m[PASS] Teste test_feedforward_com_inicializacao_dimesoes_maiores concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"\tnum_entrada: {num_entrada}, num_neuronios: {num_neuronios}")
            logging.info(f"\tEntrada (primeiros 10 elementos): {entrada[:10]}, \n\tPesos (dimensões):{np.array(pesos).shape}, \n\tBias (dimensões): {np.array(bias).shape}")
            logging.info(f"\tSaída (primeiros 5 elementos): {saida_calculada_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward_com_inicializacao_dimesoes_maiores falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha

    def test_feedforward_camada_escondida_com_bias(self):
        try:
            # Camada Escondida
            num_entradas_camada_escondida = 3
            num_neuronios_camada_escondida = 3
            pesos_camada_escondida, bias_camada_escondida = inicializacao_dos_pesos(num_entradas_camada_escondida, num_neuronios_camada_escondida)
            entrada_camada_escondida = [0.1, 0.2, 0.3]

            somatorios_entradas, saida_camada_escondida = feedforward(entrada_camada_escondida, pesos_camada_escondida, bias_camada_escondida)
            saida_camada_escondida_round = arredondar_lista(saida_camada_escondida)

            # Camada de Saída
            num_entradas_camada_saida = num_neuronios_camada_escondida
            num_neuronios_camada_saida = 2
            pesos_camada_saida, bias_camada_saida = inicializacao_dos_pesos(num_entradas_camada_saida, num_neuronios_camada_saida)

            somatorios_entradas, saida_camada_saida = feedforward(saida_camada_escondida, pesos_camada_saida, bias_camada_saida)

            saida_camada_saida_round = arredondar_lista(saida_camada_saida)

            # Verifica se a saída da camada de saída tem o tamanho correto
            self.assertEqual(len(saida_camada_saida), num_neuronios_camada_saida)

            logging.info("\033[92m[PASS] Teste test_feedforward_camada_escondida_com_bias concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"Camada Escondida - \n\tEntrada: {entrada_camada_escondida}, \n\tPesos: {np.array(pesos_camada_escondida).shape}, \n\tBias: {np.array(bias_camada_escondida).shape}")
            logging.info(f"Camada Escondida - \n\tSaída: {saida_camada_escondida_round}")
            logging.info(f"Camada de Saída - \n\tPesos: {np.array(pesos_camada_saida).shape}, \n\tBias: {np.array(bias_camada_saida).shape}")
            logging.info(f"Camada de Saída - \n\tSaída: {saida_camada_saida_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward_camada_escondida_com_bias falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha
    def test_feedforward_camada_escondida_dimensoes_maiores(self):
        try:
            # Camada Escondida
            num_entradas_camada_escondida = 120
            num_neuronios_camada_escondida = 30
            pesos_camada_escondida, bias_camada_escondida = inicializacao_dos_pesos(num_entradas_camada_escondida, num_neuronios_camada_escondida)
            entrada_camada_escondida = [0.1, 0.2, 0.3] * 40  # Cria uma entrada de 120 elementos
            somatorios_entradas, saida_camada_escondida = feedforward(entrada_camada_escondida, pesos_camada_escondida, bias_camada_escondida)
            saida_camada_escondida_round = arredondar_lista(saida_camada_escondida[:5])

            # Camada de Saída
            num_entradas_camada_saida = num_neuronios_camada_escondida
            num_neuronios_camada_saida = 7
            pesos_camada_saida, bias_camada_saida = inicializacao_dos_pesos(num_entradas_camada_saida, num_neuronios_camada_saida)

            somatorios_entradas, saida_camada_saida = feedforward(saida_camada_escondida, pesos_camada_saida, bias_camada_saida)
            saida_camada_saida_round = arredondar_lista(saida_camada_saida)

            # Verifica se a saída da camada de saída tem o tamanho correto
            self.assertEqual(len(saida_camada_saida), num_neuronios_camada_saida)

            logging.info("\033[92m[PASS] Teste test_feedforward_camada_escondida_dimensoes_maiores concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"Camada Escondida - \n\tEntrada (primeiros 10 elementos): {entrada_camada_escondida[:10]}, \n\tPesos: {np.array(pesos_camada_escondida).shape}, \n\tBias: {np.array(bias_camada_escondida).shape}")
            logging.info(f"Camada Escondida - \n\tSaída (primeiros 5 elementos): {saida_camada_escondida_round}")
            logging.info(f"Camada Saída - \n\tSaída: {saida_camada_saida_round}")
            logging.error(f"\033[91m[ERROR] Teste test_feedforward_camada_escondida_dimensoes_maiores falhou: {e}\033[0m")
            raise  # Re-lança a exceção para que o unittest reporte a falha
if __name__ == '__main__':
    unittest.main()