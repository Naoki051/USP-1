import client

data = {
    "ip": "127.0.0.1",
    "port": 9009,
    "clock": 0,
    "files_path":'./arquivos',
    'vizinhos': []
}

def exibir_menu():
    while True:
        print("Escolha um comando: ")
        print("[1] Listar peers")
        print("[2] Obter peers")
        print("[3] Listar arquivos locais")
        print("[4] Buscar arquivos")
        print("[5] Exibir estatisticas")
        print("[6] Alterar tamanho de chunk")
        print("[9] Sair")
        data["vizinhos"] = client.dict_vizinhos()
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
        elif opcao == '9':
            break



exibir_menu()