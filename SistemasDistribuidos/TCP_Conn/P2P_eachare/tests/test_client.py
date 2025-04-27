import socket, tempfile,os
import threading
import unittest
from modules.client import *
def servidor_teste(endereco, porta, mensagem_recebida):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((endereco, porta))
        server_socket.listen(1)
        try:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    mensagem_recebida["mensagem"] = data.decode() #armazena a mensagem recebida
                    conn.sendall(data)
        except Exception as e:
            print(f"Exceção: {e}")

class TestCliente(unittest.TestCase):
    def setUp(self):
        self.peer = {
            "endereco": "127.0.0.1",
            "porta": 12345,
            "clock": 1,
            'vizinhos': [("127.0.0.1", 12348, 'ONLINE')] 
        }
        self.endereco_servidor = "127.0.0.1"
        self.porta_servidor = 12347
        self.mensagem_recebida = {} #dicionario para armazenar a mensagem recebida
        self.server_thread = threading.Thread(target=servidor_teste, args=(self.endereco_servidor, self.porta_servidor, self.mensagem_recebida))
        self.server_thread.daemon = True
        self.server_thread.start()

    def test_send_message_success(self):
        mensagem_enviada = send_menssage(self.peer, self.endereco_servidor, self.porta_servidor, "TEST", "args")
        mensagem_esperada = f'{self.peer["endereco"]}:{self.peer["porta"]} {self.peer["clock"]} TEST args'
        self.assertEqual(mensagem_enviada, mensagem_esperada) #verifica se a mensagem recebida é a esperada

    def test_send_no_conn_exception(self):
        resp = send_menssage(self.peer, "127.0.0.1", 12348, "TEST", "args")
        self.assertTrue(resp)

class TestProcessaPeerList(unittest.TestCase):

    def setUp(self):
        # Cria um arquivo temporário vizinhos.txt
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')
        self.temp_file_name = self.temp_file.name
        self.temp_file.close()

        self.peer = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'vizinhos_file': self.temp_file_name,  # Usa o arquivo temporário
            'vizinhos': [
                ('192.168.1.1', '8080', 'OFFLINE'),
                ('192.168.1.2', '8081', 'ONLINE')
            ]
        }
        self.rep_args = [
            '127.0.0.1:9000:ONLINE:0',
            '192.168.1.3:8082:ONLINE:0',
            '192.168.1.2:8081:OFFLINE:0'
        ]

    def tearDown(self):
        # Remove o arquivo temporário
        os.remove(self.temp_file_name)

    def test_nao_atualiza_status_peer(self):
        processa_peer_list(self.peer, self.rep_args)
        self.assertEqual(self.peer['vizinhos'][0][2], 'OFFLINE')

    def test_nao_adiciona_vizinho_existente(self):
        processa_peer_list(self.peer, self.rep_args)
        self.assertEqual(len(self.peer['vizinhos']), 3)

    def test_rep_args_vazio(self):
        rep_args_vazio = ['127.0.0.1:9000']
        processa_peer_list(self.peer, rep_args_vazio)
        self.assertEqual(len(self.peer['vizinhos']), 2)

class TestAdicionaVizinho(unittest.TestCase):

    def setUp(self):
        # Cria um arquivo temporário para vizinhos.txt
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')
        self.temp_file_name = self.temp_file.name
        self.temp_file.close()

        self.peer = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'vizinhos_file': self.temp_file_name,
            'vizinhos': []
        }

    def tearDown(self):
        # Remove o arquivo temporário
        os.remove(self.temp_file_name)

    def test_adiciona_vizinho_arquivo(self):
        adiciona_vizinho(self.peer, '192.168.1.1', '8080', 'ONLINE')
        with open(self.temp_file_name, 'r') as arquivo_vizinhos:
            conteudo = arquivo_vizinhos.read()
            self.assertIn('192.168.1.1:8080', conteudo)

    def test_adiciona_vizinho_peer(self):
        adiciona_vizinho(self.peer, '192.168.1.1', '8080', 'ONLINE')
        self.assertEqual(self.peer['vizinhos'], [('192.168.1.1', '8080', 'ONLINE')])

class TestAtualizaStatusVizinho(unittest.TestCase):

    def setUp(self):
        # Cria um arquivo temporário para vizinhos.txt
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')
        self.temp_file_name = self.temp_file.name
        self.temp_file.close()

        self.peer = {
            'endereco': '127.0.0.1',
            'porta': 9000,
            'vizinhos_file': self.temp_file_name,
            'vizinhos': [
                ('192.168.1.1', '8080', 'OFFLINE'),
                ('192.168.1.2', '8081', 'ONLINE')
            ]
        }

    def tearDown(self):
        # Remove o arquivo temporário
        os.remove(self.temp_file_name)

    def test_atualiza_status_existente(self):
        atualiza_status_vizinho(self.peer, '192.168.1.1', '8080', 'ONLINE')
        self.assertEqual(self.peer['vizinhos'][0][2], 'ONLINE')

    def test_adiciona_novo_vizinho(self):
        atualiza_status_vizinho(self.peer, '192.168.1.3', '8082', 'ONLINE')
        self.assertEqual(self.peer['vizinhos'][2], ('192.168.1.3', '8082', 'ONLINE'))
        
class TestProcessarLsList(unittest.TestCase):

    def test_lista_vazia(self):
        resp_args = "0"
        endereco_origem = "192.168.1.10"
        porta_origem = 12345
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        self.assertEqual(resultado, [])

    def test_um_arquivo(self):
        resp_args = "1 arquivo1:1024"
        endereco_origem = "10.0.0.5"
        porta_origem = 54321
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [{'nome': 'arquivo1', 'tamanho': 1024, 'peer': '10.0.0.5:54321'}]
        self.assertEqual(resultado, esperado)

    def test_multiplos_arquivos(self):
        resp_args = "3 musica.mp3:5120 imagem.jpg:2048 documento.pdf:4096"
        endereco_origem = "200.10.5.20"
        porta_origem = 8080
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [
            {'nome': 'musica.mp3', 'tamanho': 5120, 'peer': '200.10.5.20:8080'},
            {'nome': 'imagem.jpg', 'tamanho': 2048, 'peer': '200.10.5.20:8080'},
            {'nome': 'documento.pdf', 'tamanho': 4096, 'peer': '200.10.5.20:8080'}
        ]
        self.assertEqual(resultado, esperado)

    def test_arquivo_sem_tamanho(self):
        resp_args = "1 arquivo_sem_tamanho:"
        endereco_origem = "172.16.0.1"
        porta_origem = 9000
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [{'nome': 'arquivo_sem_tamanho', 'tamanho': 0, 'peer': '172.16.0.1:9000'}]
        self.assertEqual(resultado, esperado)

    def test_arquivo_com_tamanho_invalido(self):
        resp_args = "1 arquivo_invalido:abc"
        endereco_origem = "192.168.100.50"
        porta_origem = 11111
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [{'nome': 'arquivo_invalido', 'tamanho': 0, 'peer': '192.168.100.50:11111'}]
        self.assertEqual(resultado, esperado)

    def test_arquivo_com_nome_vazio(self):
        resp_args = "1 :123"
        endereco_origem = "10.1.1.1"
        porta_origem = 22222
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [{'nome': '', 'tamanho': 123, 'peer': '10.1.1.1:22222'}]
        self.assertEqual(resultado, esperado)

    def test_multiplos_arquivos_com_diferentes_formatos(self):
        resp_args = "3 arq1:10 arq2: texto arq3:"
        endereco_origem = "200.200.200.200"
        porta_origem = 33333
        resultado = processar_ls_list(resp_args, endereco_origem, porta_origem)
        esperado = [
            {'nome': 'arq1', 'tamanho': 10, 'peer': '200.200.200.200:33333'},
            {'nome': 'arq2', 'tamanho': 0, 'peer': '200.200.200.200:33333'},
            {'nome': 'arq3', 'tamanho': 0, 'peer': '200.200.200.200:33333'}
        ]
        self.assertEqual(resultado, esperado)



if __name__ == '__main__':
    unittest.main()
