import unittest
from unittest.mock import patch, MagicMock
from modules.server import *

class TestServidorSimplificado(unittest.TestCase):

    def setUp(self):
        self.peer_teste = {
            "endereco": "127.0.0.1",
            "porta": 5000,
            "clock": 0,
            "vizinhos": [
                ["192.168.1.100", 8080, "OFFLINE"],
                ["192.168.1.101", 9000, "ONLINE"],
            ]
        }

    @patch('modules.utils.separar_msg')
    def test_lidar_com_conexao_get_peers(self, mock_separar_msg):
        mock_socket_conn = MagicMock()
        mock_socket_conn.recv.return_value = b"192.168.1.200:6000 1 GET_PEERS"

        mock_separar_msg.return_value = {
            "origem_ip": "192.168.1.200",
            "origem_port": 6000,
            "origem_clock": 1,
            "tipo": "GET_PEERS",
            "args": []
        }

        lidar_com_conexao(mock_socket_conn, self.peer_teste)

        mock_socket_conn.sendall.assert_called_once()

    @patch('modules.utils.separar_msg')
    def test_lidar_com_conexao_mensagem_generica(self, mock_separar_msg):
        mock_socket_conn = MagicMock()
        mock_socket_conn.recv.return_value = b"192.168.1.200:6000 1 HELLO"

        mock_separar_msg.return_value = {
            "origem_ip": "192.168.1.200",
            "origem_port": 6000,
            "origem_clock": 1,
            "tipo": "HELLO",
            "args": []
        }

        lidar_com_conexao(mock_socket_conn, self.peer_teste)

        mock_socket_conn.sendall.assert_called_once_with(b"Mensagem recebida com sucesso.")

    def test_construir_resposta_peers(self):
        mensagem = {
            "origem_ip": "192.168.1.200",
            "origem_port": 6000,
            "origem_clock": 1,
            "tipo": "GET_PEERS",
            "args": []
        }
        resposta = construir_resposta_peers(self.peer_teste, mensagem)
        esperado = "127.0.0.1:5000 0 PEER_LIST 2 192.168.1.100:8080:OFFLINE:0 192.168.1.101:9000:ONLINE:0"
        self.assertEqual(resposta, esperado)

if __name__ == '__main__':
    unittest.main()