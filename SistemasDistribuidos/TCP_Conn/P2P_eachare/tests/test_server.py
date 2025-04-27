import unittest
import socket
import threading
import time
from modules.server import *
from unittest.mock import patch, MagicMock

class TestTCPServer(unittest.TestCase):
    def setUp(self):
        self.peer1 = {
            "endereco": "127.0.0.1",
            "porta": 9000,
            "vizinhos_file": "vizinhos.txt",
            "vizinhos": [('127.0.0.1', 9001), ('127.0.0.1', 9003)],
            "diretorio_compartilhado": "arquivos",
            "clock": 0
        }
        self.server_thread1 = threading.Thread(target=start_server, args=(self.peer1,)) # Correção aqui
        self.server_thread1.daemon = True
        try:
            self.server_thread1.start()
        except OSError as e:
            self.fail(f"Falha ao iniciar o servidor: {e}")
        time.sleep(0.5)

    def test_servidor_iniciado_com_sucesso(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.peer1["endereco"], self.peer1["porta"]))
                self.assertTrue(True)
        except ConnectionRefusedError: 
            self.fail("O servidor não foi iniciado corretamente.")

    def test_servidor_encerrado(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.peer1["endereco"], self.peer1["porta"]))
                client_socket.sendall("SAIR".encode())
                time.sleep(0.5)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                with self.assertRaises(OSError) as context:
                    client_socket.connect((self.peer1["endereco"], self.peer1["porta"]))
                    client_socket.sendall("NOVA_MENSAGEM".encode())
                self.assertIn("Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente", str(context.exception))
        except:
            self.fail("O servidor não foi encerrado corretamente.")
    
    def tearDown(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.peer1["endereco"], self.peer1["porta"]))
                client_socket.sendall("SAIR".encode())
            except ConnectionRefusedError:
                pass

class TestConstruirRespostaPeers(unittest.TestCase):

    def setUp(self):
        self.peer = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'clock': 0,
            'vizinhos': [
                ('192.168.1.1', 8080, 'ONLINE'),
                ('192.168.1.2', 8081, 'OFFLINE'),
                ('192.168.1.3', 8082, 'ONLINE'),
            ]
        }
        self.mensagem_separada = {
            'endereco_origem': '192.168.1.2',
            'porta_origem': 8081,
        }

    def test_construir_resposta_peers_exclui_origem(self):
        resposta = construir_resposta_peers(self.peer, self.mensagem_separada)
        self.assertNotIn('192.168.1.2:8081:OFFLINE:0', resposta)

    def test_construir_resposta_peers_inclui_outros_vizinhos(self):
        resposta = construir_resposta_peers(self.peer, self.mensagem_separada)
        self.assertIn('192.168.1.1:8080:ONLINE:0', resposta)
        self.assertIn('192.168.1.3:8082:ONLINE:0', resposta)

    def test_construir_resposta_peers_formato_correto(self):
        resposta = construir_resposta_peers(self.peer, self.mensagem_separada)
        self.assertEqual(resposta, '127.0.0.1:9000 0 PEER_LIST 2 192.168.1.1:8080:ONLINE:0 192.168.1.3:8082:ONLINE:0')

    def test_construir_resposta_peers_sem_vizinhos(self):
        peer_sem_vizinhos = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'clock': 0,
            'vizinhos': []
        }
        resposta = construir_resposta_peers(peer_sem_vizinhos, self.mensagem_separada)
        self.assertEqual(resposta, '127.0.0.1:9000 0 PEER_LIST 0 ')

    def test_construir_resposta_peers_todos_vizinhos_origem(self):
        peer_todos_origem = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'clock': 0,
            'vizinhos': [('192.168.1.2', 8081, 'OFFLINE')]
        }
        resposta = construir_resposta_peers(peer_todos_origem, self.mensagem_separada)
        self.assertEqual(resposta, '127.0.0.1:9000 0 PEER_LIST 0 ')

class TestConnHandler(unittest.TestCase):

    def setUp(self):
        self.conn = MagicMock()
        self.peer = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'clock': 0,
            'vizinhos': [
                ('192.168.1.1', 8080, 'OFFLINE'),
                ('192.168.1.2', 8081, 'OFFLINE')
            ]
        }

    def test_sair(self):
        result = conn_handler(self.conn, self.peer, 'SAIR')
        self.assertFalse(result)

    def test_hello(self):
        mensagem = '192.168.1.1:8080 1 HELLO'
        result = conn_handler(self.conn, self.peer, mensagem)
        self.assertTrue(result)
        self.assertEqual(self.peer['vizinhos'][0][2], 'ONLINE')

    def test_get_peers(self):
        mensagem = '192.168.1.2:8081 1 GET_PEERS'
        result = conn_handler(self.conn, self.peer, mensagem)
        self.assertTrue(result)
        self.assertEqual(self.peer['vizinhos'][1][2], 'ONLINE')
        self.conn.sendall.assert_called()

    def test_bye(self):
        mensagem = '192.168.1.1:8080 1 BYE'
        result = conn_handler(self.conn, self.peer, mensagem)
        self.assertTrue(result)
        self.assertEqual(self.peer['vizinhos'][0][2], 'OFFLINE')

    def test_clock_increment(self):
        mensagem = '192.168.1.1:8080 1 HELLO'
        conn_handler(self.conn, self.peer, mensagem)
        self.assertEqual(self.peer['clock'], 1)

if __name__ == '__main__':
    unittest.main()