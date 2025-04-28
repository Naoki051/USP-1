import unittest
import threading
import os
import io
import tempfile
from modules.server import *
from modules.client import *
from unittest.mock import patch

class TestCliente(unittest.TestCase):
    def setUp(self):
        self.peer_teste = {
            "endereco": "127.0.0.1",
            "porta": 5000,
            "clock": 0,
            "vizinhos": [
                ["127.0.0.1", 8080, "OFFLINE"],
                ["127.0.0.1", 9000, "OFFLINE"]
            ],
            "diretorio_compartilhado": ""
        }
        self.vizinho_teste = {
            "endereco": "127.0.0.1",
            "porta": 9000,
            "clock": 0,
            "vizinhos": [
                ["127.0.0.1", 8080, "OFFLINE"],
                ["127.0.0.1", 9003, "OFFLINE"]
            ],
            "diretorio_compartilhado": ""
        }

    def test_cliente_hello(self):
        with patch('builtins.print') as mock_print:
            try:
                thread_servidor = threading.Thread(target=servidor, args=(self.vizinho_teste,))
                thread_cliente = threading.Thread(target=cliente, args=(self.peer_teste, self.vizinho_teste["endereco"], self.vizinho_teste["porta"], "HELLO"))
                thread_servidor.start()
                thread_cliente.start()

                thread_cliente.join()
                thread_servidor.join()

                calls = [call[0][0] for call in mock_print.call_args_list]
                self.assertIn(f'Encaminhando mensagem: "{self.peer_teste["endereco"]}:{self.peer_teste["porta"]} {self.peer_teste["clock"]} HELLO para 127.0.0.1:9000"', calls)
                self.assertIn(f"Mensagem recebida: {self.peer_teste['endereco']}:{self.peer_teste['porta']} {self.peer_teste['clock']} HELLO para {self.vizinho_teste['endereco']}:{self.vizinho_teste['porta']}", calls)
            except Exception as e:
                self.fail(f"Ocorreu um erro durante o teste: {e}")

    def test_cliente_get_peers(self):
        with patch('builtins.print') as mock_print:
            try:
                thread_servidor = threading.Thread(target=servidor, args=(self.vizinho_teste,))
                thread_cliente = threading.Thread(target=cliente, args=(self.peer_teste, self.vizinho_teste["endereco"], self.vizinho_teste["porta"], "GET_PEERS"))
                thread_servidor.start()
                thread_cliente.start()

                thread_cliente.join()
                thread_servidor.join()

                calls = [call[0][0] for call in mock_print.call_args_list]
                self.assertIn(f'Encaminhando mensagem: "{self.peer_teste["endereco"]}:{self.peer_teste["porta"]} {self.peer_teste["clock"]} GET_PEERS para 127.0.0.1:9000"', calls)
                self.assertIn(f'Resposta recebida: "{self.vizinho_teste["endereco"]}:{self.vizinho_teste["porta"]} {self.vizinho_teste["clock"]} PEER_LIST 2 127.0.0.1:8080:OFFLINE:0 127.0.0.1:9003:OFFLINE:0"', calls)
            except Exception as e:
                self.fail(f"Ocorreu um erro durante o teste: {e}")
class TestListarArquivosLocais(unittest.TestCase):

    def setUp(self):
        # Cria um diretório temporário e arquivos de teste
        self.temp_dir = tempfile.TemporaryDirectory()
        self.diretorio_teste = self.temp_dir.name
        self.arquivo1 = os.path.join(self.diretorio_teste, "arquivo1.txt")
        self.arquivo2 = os.path.join(self.diretorio_teste, "arquivo2.txt")
        open(self.arquivo1, 'a').close()
        open(self.arquivo2, 'a').close()

    def tearDown(self):
        # Remove o diretório temporário e os arquivos
        self.temp_dir.cleanup()

    def test_listar_arquivos_com_arquivos_print_completo(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            listar_arquivos_locais(self.diretorio_teste)
            saida_esperada = "\tarquivo1.txt\n\tarquivo2.txt\n"
            self.assertEqual(mock_stdout.getvalue(), saida_esperada)


if __name__ == '__main__':
    unittest.main()