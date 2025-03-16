import socket
from client import separar_msg,incrementa_clock,dict_vizinhos

def servidor(data):
    """ Inicia um servidor TCP que aceita conexões de um único peer """
    data['vizinhos'] = dict_vizinhos()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((data['ip'], data['port']))
        while True:
            servidor_socket.listen(1)
            print(f"Servidor aguardando conexões em {data['ip']}:{data['port']}...")

            conexao, endereco = servidor_socket.accept()
            with conexao:
                print(f"Conexão estabelecida com {endereco}")
                atualizar_status_vizinho(data,endereco[0],"ONLINE")
                
                try:
                    mensagem = conexao.recv(1024).decode()
                    if not mensagem:
                        print("Mensagem vazia!")
                        # Encerra se a conexão for fechada
                    print(f"Recebido: {mensagem}")
                    mensagem = separar_msg(mensagem)
                    if mensagem['tipo'].upper() == "SAIR":
                        print("Encerrando conexão servidor...")
                        conexao.sendall("SAIR".encode())  # Confirma o encerramento
                        break
                    elif mensagem['tipo'].upper() == "GET_PEERS":
                        resposta = f"{data['ip']}:{data['port']} {data['clock']} PEER_LIST {len(data['vizinhos'])-1} "

                        for vizinho in data['vizinhos']:
                            if vizinho['ip'] != mensagem['origem_ip'] or vizinho['port'] != mensagem['origem_port']:
                                resposta += f"{vizinho['ip']}:{vizinho['port']}:{vizinho['status']}:0 "
                        incrementa_clock(data)
                        conexao.send(resposta.encode())
                    elif mensagem['tipo'].upper() == "BYE":
                        atualizar_status_vizinho(data, mensagem['origem_ip'],"OFFLINE")
                except Exception as e:
                    print(f"Erro na conexão: {e}")
                
    print(f"Servidor finalizado.")

def atualizar_status_vizinho(data, endereco,status):
    """Atualiza o status do vizinho para status se o IP corresponder."""
    for index, vizinho in enumerate(data['vizinhos']):
        if vizinho['ip'] == endereco:
            if vizinho['status'] != status:
                vizinho['status'] = status
                print(f"Status do vizinho {vizinho['ip']}:{vizinho['port']} atualizado para {status}.")
            return  # Encerra a função após encontrar e atualizar o vizinho

    print(f"Nenhum vizinho encontrado com o IP {endereco}.")