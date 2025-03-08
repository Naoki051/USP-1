import os
import socket

class Peer:
    def __init__(self, host, port, file_name="vizinhos.txt"):
        self.host = host
        self.port = port
        self.status = 'OFFLINE'
        self.peers_vizinhos = []
        self.files_path = "./arquivos"
        self.clock = 0
        self.load_peers_vizinhos(file_name)

    def txt_to_str_list(self, filename):
        try:
            with open(filename, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def load_peers_vizinhos(self, filename):
        vizinhos = self.txt_to_str_list(filename)
        if not vizinhos:
            return
        for peer_str in vizinhos:
            try:
                host, port_str = peer_str.split(":")
                port = int(port_str)
                # Evitar recursão infinita: não criar Peer dentro de Peer
                self.peers_vizinhos.append((host, port)) #adicionando uma tupla com host e porta.
            except Exception as e:
                print(f"Erro inesperado ao adicionar peer '{peer_str}': {e}")

    @staticmethod
    def send_msg_to(peer_host, peer_port, msg):
        try:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((peer_host, peer_port))
            print(f"Mensagem: {msg}")
            cliente_socket.send(msg.encode())
            cliente_socket.close()
        except Exception as e:
            print(f"Erro: {e}")

    def get_files_names(self):
        try:
            arquivos = os.listdir(self.files_path)
            if not arquivos:
                print("Nenhum arquivo encontrado.")
                return [] #retornando uma lista vazia.
            else:
                return arquivos
        except FileNotFoundError:
            print("Erro: O diretório especificado não foi encontrado.")
            return []
        except PermissionError:
            print("Erro: Permissão negada para acessar o diretório.")
            return []

peer = Peer('127.0.0.1', 9000, "vizinhos.txt")
peer1 = Peer('127.0.0.1', 9001, "")
peer.send_msg_to(peer1.host,peer1.port,"PEER_LIST")
arquivos = peer.get_files_names()
if arquivos: #verifica se a lista não está vazia.
    for arquivo in arquivos:
        print(f"- {arquivo}")