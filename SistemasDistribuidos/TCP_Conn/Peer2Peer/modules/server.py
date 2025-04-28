import socket
from modules.utils import *

def servidor(peer):
    try:
        endereco = peer['endereco']
        porta = peer['porta']
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((endereco, porta))
            running = True
            while running:
                server_socket.listen()
                conn, addr = server_socket.accept()
                with conn:
                    running = lidar_com_conexao(conn, peer)
    except Exception as e:
        print(f"Erro no servidor: {e}")

def lidar_com_conexao(conn, peer):
    try:
        data = conn.recv(1024)
        if data:
            mensagem = data.decode()
            if mensagem and mensagem=="SAIR":
                return False
            
            print(f"Mensagem recebida: {mensagem}")
            mensagem = separar_msg(data.decode())
            
            if mensagem and mensagem['tipo'] == 'GET_PEERS':
                resposta = construir_resposta_peers(peer, mensagem)
                atualiza_status_vizinho(peer,mensagem['endereco_origem'],mensagem['porta_origem'],'ONLINE')
                incrementa_clock(peer)
                print(f'Encaminhando resposta: "{resposta}"')
                conn.sendall(resposta.encode())
                return True
            elif mensagem and mensagem['tipo'] == 'BYE':
                atualiza_status_vizinho(peer,mensagem['endereco_origem'],mensagem['porta_origem'],'OFFLINE')
                return True
            atualiza_status_vizinho(peer,mensagem['endereco_origem'],mensagem['porta_origem'],'ONLINE')
    except Exception as e:
        print(f"Erro ao lidar com a conexão: {e}")

def construir_resposta_peers(peer, mensagem):
    vizinhos_formatados = []
    for vizinho in peer['vizinhos']:
        if vizinho[0] != mensagem['endereco_origem'] or vizinho[1] != mensagem['porta_origem']:
            vizinhos_formatados.append(f"{vizinho[0]}:{vizinho[1]}:{vizinho[2]}:0")
    resposta = f"{peer['endereco']}:{peer['porta']} {peer['clock']} PEER_LIST {len(vizinhos_formatados)} {' '.join(vizinhos_formatados)}"
    return resposta