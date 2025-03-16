import socket, os
from client import separar_msg,incrementa_clock,dict_vizinhos

def servidor(data):
    """ Inicia um servidor TCP que aceita conexões de um único peer """
    data['vizinhos'] = dict_vizinhos()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((data['ip'], data['port']))
        while True:
            servidor_socket.listen(1)
            conexao, endereco = servidor_socket.accept()
            with conexao:
                try:
                    mensagem = conexao.recv(1024).decode()
                    if mensagem.upper() == "SAIR":
                        print("Encerrando conexão servidor...")
                        break
                    print(f"Mensagem recebida: {mensagem}")
                    mensagem = separar_msg(mensagem)

                    if mensagem['tipo'].upper() == "HELLO":
                        atualizar_status_vizinho(data,mensagem['origem_ip'],mensagem['origem_port'],"ONLINE")
                    elif mensagem['tipo'].upper() == "BYE":
                        atualizar_status_vizinho(data, mensagem['origem_ip'],mensagem['origem_port'],"OFFLINE")
                    elif mensagem['tipo'].upper() == "GET_PEERS":
                        resposta = f"{data['ip']}:{data['port']} {data['clock']} PEER_LIST {len(data['vizinhos'])-1} "
                        for vizinho in data['vizinhos']:
                            if vizinho['ip'] != mensagem['origem_ip'] or vizinho['port'] != mensagem['origem_port']:
                                resposta += f"{vizinho['ip']}:{vizinho['port']}:{vizinho['status']}:0 "
                        incrementa_clock(data)
                        conexao.send(resposta.encode())
                    
                except Exception as e:
                    print(f"Erro na conexão.")
                
    print(f"Servidor finalizado.")

def atualizar_status_vizinho(data, ip, port, status):
    """Atualiza o status do vizinho para status se o IP:PORT corresponder."""
    vizinho_encontrado = False  # Flag para verificar se algum vizinho foi encontrado
    for index, vizinho in enumerate(data['vizinhos']):
        if vizinho['ip'] == ip and vizinho['port'] == port:
            if vizinho['status'] != status:
                vizinho['status'] = status
                print(f"Status do vizinho {vizinho['ip']}:{vizinho['port']} atualizado para {status}.")
            vizinho_encontrado = True  # Define a flag como True se um vizinho for encontrado
    if not vizinho_encontrado:
        print(f"Nenhum vizinho encontrado com o IP:PORT {ip}:{port}.")
