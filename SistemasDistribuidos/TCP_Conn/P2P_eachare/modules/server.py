import socket
from modules.utils import *

def start_server(peer):
    """
    Inicia o servidor P2P para receber e processar conexões de outros peers.
    """
    endereco = peer['endereco']
    porta = peer['porta']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((endereco, porta))
            running = True
            while running:
                server_socket.listen()
                conn, addr = server_socket.accept()
                with conn:
                    mensagem = conn.recv(1024).decode()
                    if mensagem:
                        running = conn_handler(conn,peer,mensagem)
    except Exception as e:
        print(f"Erro: {e}")
    
def conn_handler(conn,peer,mensagem):
    """
    Processa mensagens recebidas de outros peers e executa ações apropriadas.
    """
    if mensagem == 'SAIR':
        return False
    print(f"Mensagem recebida: {mensagem}")
    incrementa_clock(peer)
    mensagem_partes = separar_msg(mensagem)
    endereco_origem = mensagem_partes['endereco_origem']
    porta_origem = mensagem_partes['porta_origem']
    tipo = mensagem_partes['tipo']
    if tipo == 'HELLO':
        atualiza_status_vizinho(peer,endereco_origem,porta_origem,'ONLINE')
    elif tipo == 'GET_PEERS':
        atualiza_status_vizinho(peer,endereco_origem,porta_origem,'ONLINE')
        incrementa_clock(peer)
        resposta = construir_resposta_peers(peer, mensagem_partes)
        print(f'Encaminhando resposta: "{resposta}"')
        conn.sendall(resposta.encode())
    elif tipo == 'BYE':
        atualiza_status_vizinho(peer,endereco_origem,porta_origem,'OFFLINE')
    return True

def construir_resposta_peers(peer, mensagem_separada):
    """
    Constrói uma resposta contendo a lista de vizinhos do peer, com excessão do peer de origem.
    """
    vizinhos_formatados = []
    for vizinho in peer['vizinhos']:
        if vizinho[0] != mensagem_separada['endereco_origem'] or vizinho[1] != mensagem_separada['porta_origem']:
            vizinhos_formatados.append(f"{vizinho[0]}:{vizinho[1]}:{vizinho[2]}:0")
    resposta = f"{peer['endereco']}:{peer['porta']} {peer['clock']} PEER_LIST {len(vizinhos_formatados)} {' '.join(vizinhos_formatados)}"
    return resposta