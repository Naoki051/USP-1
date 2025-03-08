import os
import socket
from peer import Peer

self_host = "127.0.0.1"
self_port = 9000
clock = 0

def send_msg_to(host,port,msg):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host,int(port)))
        print(f"Mensagem: {msg}")
        cliente_socket.send(msg.encode())

        cliente_socket.close()

    
    except Exception as e:
        print(f"Erro: {e}")


def txt_to_str_list(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]
    

def exibir_menu():
    print("[1] Listar peers")
    print("[2] Obter peers")
    print("[3] Listar arquivos locais")
    print("[4] Buscar arquivos")
    print("[5] Exibir estatísticas")
    print("[6] Alterar tamanho de chunk")
    print("[9] Sair")

     
def exibir_menu_listar(peer: Peer):
    print("Lista de peers:")
    print(f"[1] Voltar ao menu anterior")
    
    # Exibir lista de vizinhos começando da opção 2
    for index, vizinho, status in enumerate(peer.peers_vizinhos, start=2):
        print(f"[{index}] {vizinho.host}:{vizinho.port} {status}")


def listar_peers(peer: Peer):
    exibir_menu_listar(peer)
    while True:
        opcao = input("Escolha uma opção: ")

        # Voltar ao menu anterior
        if opcao == '1':
            break
        try:
            opcao_int = int(opcao)
            
            # Verifica se a opção está dentro do intervalo válido
            if 2 <= opcao_int < 2 + len(peer.peers_vizinhos):
                host, port = peer.peers_vizinhos[opcao_int - 2].split(":")  # Supondo que cada vizinho seja "host:porta"
                mensagem = f"{self_host}:{self_port} {clock} HELLO"
                peer.send_msg_to(host,port)
            else:
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("Entrada inválida. Digite um número.")
    

def obter_peers(peer: Peer):
    print("Obtendo peers...")
    for vizinho in peer.peers_vizinhos:
        mensagem = f"{self_host}:{self_port} {clock} PEER_LIST"
        host, port = vizinho.split(":")  # Supondo que cada vizinho seja "host:porta"
        peer.send_msg_to(host, port, mensagem)


def listar_arquivos_locais(peer: Peer):
    arquivos = peer.get_files_names()
    if arquivos: 
        for arquivo in arquivos:
            print(f"- {arquivo}")


def buscar_arquivos():
    print("Buscando arquivos...")
    # Aqui você pode adicionar a lógica para buscar arquivos de outros peers

def exibir_estatisticas():
    print("Exibindo estatísticas...")
    # Aqui você pode adicionar a lógica para exibir estatísticas

def alterar_tamanho_chunk():
    novo_tamanho = input("Digite o novo tamanho de chunk: ")
    print(f"Tamanho de chunk alterado para {novo_tamanho}")
    # Aqui você pode adicionar a lógica para alterar o tamanho do chunk

def main():
    peer = Peer(self_host,self_port)
    vizinhos = txt_to_str_list("vizinhos.txt")
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            listar_peers(peer)
        elif opcao == '2':
            obter_peers(vizinhos)
        elif opcao == '3':
            listar_arquivos_locais("./arquivos")
        elif opcao == '4':
            buscar_arquivos()
        elif opcao == '5':
            exibir_estatisticas()
        elif opcao == '6':
            alterar_tamanho_chunk()
        elif opcao == '9':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
