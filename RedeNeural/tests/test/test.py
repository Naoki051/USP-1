import unittest
import numpy as np
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from rede_neural import backpropagation
class TestBackpropagation(unittest.TestCase):
    def test_backpropagation_atualiza_parametros(self):
        try:
            entradas = [0.5, 0.3]
            pesos_oculta = [[0.1, 0.2], [0.4, 0.3]]
            biases_oculto = [0.1, -0.2]
            pesos_saida = [[0.3, 0.5], [0.7, -0.1]]
            biases_saida = [0.2, -0.3]
            alvos = [0.4, 0.6]
            taxa_aprendizagem = 0.1

            novos_pesos_oculta, novos_biases_oculta, novos_pesos_saida, novos_biases_saida = backpropagation(
                entradas, pesos_oculta, biases_oculto, pesos_saida, biases_saida, alvos, taxa_aprendizagem
            )

            # Verificações básicas de forma
            self.assertEqual(len(novos_pesos_oculta), len(pesos_oculta))
            self.assertEqual(len(novos_biases_oculta), len(biases_oculto))
            self.assertEqual(len(novos_pesos_saida), len(pesos_saida))
            self.assertEqual(len(novos_biases_saida), len(biases_saida))

            # Verifica que foram atualizados
            self.assertNotEqual(novos_pesos_oculta, pesos_oculta)
            self.assertNotEqual(novos_pesos_saida, pesos_saida)

            # Verifica que os valores estão entre -1 e 1
            for camada in novos_pesos_oculta + novos_pesos_saida:
                for peso in camada:
                    self.assertTrue(-1 <= peso <= 1)

            for bias in novos_biases_oculta + novos_biases_saida:
                self.assertTrue(-1 <= bias <= 1)

            logging.info("\033[92m[PASS] Teste test_backpropagation_atualiza_parametros concluído com sucesso\033[0m")
        except AssertionError as e:
            logging.info(f"Entradas: {entradas}")
            logging.info(f"Pesos oculta (antes): {pesos_oculta}")
            logging.info(f"Pesos saída (antes): {pesos_saida}")
            logging.error(f"\033[91m[ERROR] Teste test_backpropagation_atualiza_parametros falhou: {e}\033[0m")
            raise  # Re-lança exceção para o unittest reportar

if __name__ == '__main__':
    unittest.main()