import threading, unittest, time, socket
from modules.server import start_server
from modules.client import send_menssage

class TestCliente(unittest.TestCase):
    def setUp(self):
        self.peer1 = {
            "endereco": "127.0.0.1",
            "porta": 9000,
            "vizinhos_file": "vizinhos.txt",
            "vizinhos": [('127.0.0.1', 9001,'OFFLINE'), ('127.0.0.1', 9003,'OFFLINE')],
            "diretorio_compartilhado": "arquivos",
            "clock": 0
        }

        self.peer2 = {
            "endereco": "127.0.0.1",
            "porta": 9001,
            "vizinhos_file": "vizinhos.txt",
            "vizinhos": [('127.0.0.1', 9000,'OFFLINE'), ('127.0.0.1', 9002,'OFFLINE'), ('127.0.0.1', 9004,'OFFLINE')],
            "diretorio_compartilhado": "arquivos",
            "clock": 0
        }

        self.server_thread1 = threading.Thread(target=start_server, args=(self.peer1,))
        self.server_thread1.daemon = True
        self.server_thread2 = threading.Thread(target=start_server, args=(self.peer2,))
        self.server_thread2.daemon = True

        try:
            self.server_thread1.start()
            self.server_thread2.start()
        except OSError as e:
            self.fail(f"Falha ao iniciar o servidor: {e}")
        time.sleep(0.5)

    def test_hello(self):
        try:
            resposta = send_menssage(self.peer2, self.peer1['endereco'], self.peer1['porta'], "HELLO")
            self.assertIn("127.0.0.1:9001 1 HELLO", resposta) # Exemplo de verificação
        except OSError as e:
            self.fail(f"Erro na comunicação: {e}")

    def test_get_peers(self):
        try:
            resposta = send_menssage(self.peer2, self.peer1['endereco'], self.peer1['porta'], "GET_PEERS")
            self.assertIn("127.0.0.1:9001 1 GET_PEERS", resposta) # Exemplo de verificação
        except OSError as e:
            self.fail(f"Erro na comunicação: {e}")
    

    def tearDown(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.peer1["endereco"], self.peer1["porta"]))
                client_socket.sendall("SAIR".encode())
        except ConnectionRefusedError:
            pass  # Ignora a exceção se o servidor já estiver encerrado

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.peer2["endereco"], self.peer2["porta"]))
                client_socket.sendall("SAIR".encode())
        except ConnectionRefusedError:
            pass  # Ignora a exceção se o servidor já estiver encerrado