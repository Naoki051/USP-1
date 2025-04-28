import unittest
import os,io,sys
from modules.utils import *

class TestValidacoes(unittest.TestCase):

    def setUp(self):
        # Cria arquivos e diretórios de teste
        with open("teste_vizinhos.txt", "w") as f:
            f.write("127.0.0.1:8080\n")
            f.write("127.0.0.1:9090\n")
        os.makedirs("teste_diretorio", exist_ok=True)

    def tearDown(self):
        # Remove arquivos e diretórios de teste
        os.remove("teste_vizinhos.txt")
        os.rmdir("teste_diretorio")

    def test_validar_endereco_porta_valido(self):
        endereco, porta = validar_endereco_porta("127.0.0.1:8080")
        self.assertEqual(endereco, "127.0.0.1")
        self.assertEqual(porta, 8080)

    def test_validar_endereco_porta_invalido(self):
        with self.assertRaises(ValidacaoErro):
            validar_endereco_porta("endereco_invalido")

    def test_validar_arquivo_existente(self):
        self.assertIsNone(validar_arquivo("teste_vizinhos.txt"))

    def test_validar_arquivo_nao_existente(self):
        with self.assertRaises(ValidacaoErro):
            validar_arquivo("arquivo_inexistente.txt")

    def test_validar_diretorio_existente(self):
        self.assertIsNone(validar_diretorio("teste_diretorio"))

    def test_validar_diretorio_nao_existente(self):
        with self.assertRaises(ValidacaoErro):
            validar_diretorio("diretorio_inexistente")

class TestVizinhosTxtToList(unittest.TestCase):

    def setUp(self):
        # Cria arquivos de teste
        self.arquivo_valido = "vizinhos_valido.txt"
        with open(self.arquivo_valido, "w") as f:
            f.write("127.0.0.1:8080\n")
            f.write("192.168.1.100:5000\n")
            f.write("localhost:9000\n")

        self.arquivo_portas_invalidas = "vizinhos_portas_invalidas.txt"
        with open(self.arquivo_portas_invalidas, "w") as f:
            f.write("127.0.0.1:abc\n")
            f.write("192.168.1.100:5000\n")

        self.arquivo_linhas_mal_formatadas = "vizinhos_linhas_mal_formatadas.txt"
        with open(self.arquivo_linhas_mal_formatadas, "w") as f:
            f.write("127.0.0.1\n")
            f.write("192.168.1.100:5000\n")
            f.write("endereco:porta:extra\n")

        self.arquivo_vazio = "vizinhos_vazio.txt"
        open(self.arquivo_vazio, "w").close()

    def tearDown(self):
        # Remove arquivos de teste
        os.remove(self.arquivo_valido)
        os.remove(self.arquivo_portas_invalidas)
        os.remove(self.arquivo_linhas_mal_formatadas)
        os.remove(self.arquivo_vazio)

    def test_arquivo_valido(self):
        esperado = [("127.0.0.1", 8080, "OFFLINE"), ("192.168.1.100", 5000, "OFFLINE"), ("localhost", 9000, "OFFLINE")]
        resultado = vizinhos_txt_to_list(self.arquivo_valido)
        self.assertEqual(resultado, esperado)

    def test_arquivo_portas_invalidas(self):
        esperado = [("192.168.1.100", 5000, "OFFLINE")]
        resultado = vizinhos_txt_to_list(self.arquivo_portas_invalidas)
        self.assertEqual(resultado, esperado)

    def test_arquivo_linhas_mal_formatadas(self):
        esperado = [("192.168.1.100", 5000, "OFFLINE")]
        resultado = vizinhos_txt_to_list(self.arquivo_linhas_mal_formatadas)
        self.assertEqual(resultado, esperado)

    def test_arquivo_vazio(self):
        esperado = []
        resultado = vizinhos_txt_to_list(self.arquivo_vazio)
        self.assertEqual(resultado, esperado)

    def test_arquivo_nao_existente(self):
        esperado = []
        resultado = vizinhos_txt_to_list("arquivo_inexistente.txt")
        self.assertEqual(resultado, esperado)

class TestAtualizaStatusVizinho(unittest.TestCase):

    def setUp(self):
        self.peer_teste = {
            "vizinhos": [
                ["192.168.1.100", 8080, "OFFLINE"],
                ["192.168.1.101", 9000, "OFFLINE"],
            ]
        }

    def test_atualiza_status_vizinho_sucesso(self):
        atualiza_status_vizinho(self.peer_teste, "192.168.1.100", 8080, "ONLINE")
        self.assertEqual(self.peer_teste["vizinhos"][0][2], "ONLINE")

    def test_atualiza_status_vizinho_vizinho_nao_encontrado(self):
        atualiza_status_vizinho(self.peer_teste, "192.168.1.200", 7000, "ONLINE")
        self.assertEqual(self.peer_teste["vizinhos"][0][2], "OFFLINE")
        self.assertEqual(self.peer_teste["vizinhos"][1][2], "OFFLINE")

    def test_atualiza_status_vizinho_peer_vazio(self):
        peer_vazio = {"vizinhos": []}
        atualiza_status_vizinho(peer_vazio, "192.168.1.100", 8080, "ONLINE")
        self.assertEqual(peer_vazio["vizinhos"], [])

    def test_atualiza_status_vizinho_peer_sem_vizinhos(self):
        peer_sem_vizinhos = {}
        buffer_saida = io.StringIO()
        sys.stdout = buffer_saida
        atualiza_status_vizinho(peer_sem_vizinhos, "192.168.1.100", 8080, "ONLINE")
        sys.stdout = sys.__stdout__
        self.assertIn("Erro: 'vizinhos' não encontrado no dicionário peer.", buffer_saida.getvalue())
    
class TestSepararMsg(unittest.TestCase):

    def test_mensagem_valida_com_args(self):
        mensagem = "192.168.1.100:8080 1234 PEER_LIST arg1 arg2"
        resultado = separar_msg(mensagem)
        esperado = {
            "origem_ip": "192.168.1.100",
            "origem_port": 8080,
            "origem_clock": 1234,
            "tipo": "PEER_LIST",
            "args": ["arg1", "arg2"]
        }
        self.assertEqual(resultado, esperado)

    def test_mensagem_valida_sem_args(self):
        mensagem = "127.0.0.1:5000 5678 HELLO"
        resultado = separar_msg(mensagem)
        esperado = {
            "origem_ip": "127.0.0.1",
            "origem_port": 5000,
            "origem_clock": 5678,
            "tipo": "HELLO",
            "args": []
        }
        self.assertEqual(resultado, esperado)

    def test_mensagem_mal_formatada_poucas_partes(self):
        mensagem = "192.168.1.100:8080 1234"
        resultado = separar_msg(mensagem)
        self.assertIsNone(resultado)

    def test_mensagem_mal_formatada_endereco_invalido(self):
        mensagem = "192.168.1.100:abc 1234 TIPO"
        resultado = separar_msg(mensagem)
        self.assertIsNone(resultado)

    def test_mensagem_mal_formatada_clock_invalido(self):
        mensagem = "192.168.1.100:8080 abc TIPO"
        resultado = separar_msg(mensagem)
        self.assertIsNone(resultado)



if __name__ == '__main__':
    unittest.main()