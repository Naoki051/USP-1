import client, server, socket
import threading

data = {
    "ip": "127.0.0.1",
    "port": 9000,
    "clock": 0,
    "files_path":'./arquivos',
    'vizinhos': []
}

def exibir_menu():
    data["vizinhos"] = client.dict_vizinhos()
    while True:
        print("Escolha um comando: ")
        print("[1] Listar peers")
        print("[2] Obter peers")
        print("[3] Listar arquivos locais")
        print("[4] Buscar arquivos")
        print("[5] Exibir estatisticas")
        print("[6] Alterar tamanho de chunk")
        print("[9] Sair")
        opcao =  input()
        if opcao == '1':
            client.listar_vizinhos(data)
            opcao =  input()
            opcao_int = int(opcao)
            num_vizinhos = len(data['vizinhos'])

            if opcao_int == 0:
                pass  # Opção 0: não fazer nada
            elif 1 <= opcao_int <= num_vizinhos:
                client.cliente(data, opcao_int - 1, "HELLO")
        elif opcao == '2':
            for index, vizinho in enumerate(data['vizinhos']):
                client.cliente(data, index, 'GET_PEERS')
        elif opcao == '3':
            client.listar_arquivos(data)
        elif opcao == '9':
            for index, vizinho in enumerate(data['vizinhos']):
                client.cliente(data, index, 'BYE')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((data["ip"],data["port"]))
                mensagem = client.juntar_msg(data,"SAIR")
                client_socket.send(mensagem.encode())
            break

def main():
    thread_client = threading.Thread(target=exibir_menu)
    thread_server = threading.Thread(target=server.servidor,args=(data,))

    thread_server.start()
    thread_client.start()
    
    thread_server.join()
    thread_client.join()

main()