import os
import threading
import peer
from server import servidor

def exibir_menu():
    print("[1] Listar peers")
    print("[2] Obter peers")
    print("[3] Listar arquivos locais")
    print("[4] Buscar arquivos")
    print("[5] Exibir estatísticas")
    print("[6] Alterar tamanho de chunk")
    print("[9] Sair")


def listar_peers():
    print("Lista de Peers...")


def obter_peers():
    print("Obtendo peers...")

def listar_arquivos_locais(file_path="./arquivos"):
    arquivos = os.listdir(file_path)
    # Filtrando apenas arquivos (ignorando diretórios)
    arquivos = [f for f in arquivos if os.path.isfile(os.path.join(file_path, f))]
    
    print("Lista de arquivos...")
    if not arquivos:  # Verifica se a lista está vazia
        print("Vazio")
    else:
        print(arquivos)

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
    ip="127.0.0.1"
    port="9000"
    threading.Thread(target=start_peer_server, daemon=True).start()

    while True:
        command = input("Enter 'connect' to send a message, or 'exit' to stop the peer: ").strip().lower()
        if command == "connect":
            peer_ip = input("Enter peer IP: ").strip()
            peer_port = int(input("Enter peer port: ").strip())
            msg_type = input("Enter message type (e.g., PING, OUT): ").strip()
            arguments = input("Enter arguments (or leave empty): ").strip()

            connect_to_peer(peer_ip, peer_port,sender_ip,sender_port, msg_type, arguments)

        elif command == "exit":
            print("Shutting down peer...")
            break
 
 
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            listar_peers()
        elif opcao == '2':
            obter_peers()
        elif opcao == '3':
            listar_arquivos_locais()
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

main()