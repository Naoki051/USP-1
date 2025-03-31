import socket,os
from modules.utils import *
def send_menssage(peer, endereco_servidor, porta_servidor, tipo, args=''):
    """
    Envia uma mensagem para um servidor específico, processa a resposta e atualiza o status do vizinho.
    Em caso de sucesso, processa a resposta. Em caso de erro, atualiza o status do vizinho para 'OFFLINE'.
    """
    try:
        incrementa_clock(peer)
        mensagem = f'{peer["endereco"]}:{peer["porta"]} {peer["clock"]} {tipo} {args}'.strip()
        print(f'Encaminhando mensagem: "{mensagem}" para {endereco_servidor}:{porta_servidor}')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((endereco_servidor, porta_servidor))
            
            client_socket.sendall(mensagem.encode())
            if tipo == 'BYE':
                return mensagem
            elif tipo == 'HELLO':
                atualiza_status_vizinho(peer, endereco_servidor, porta_servidor,'ONLINE')
                return mensagem
            elif tipo == 'GET_PEERS':
                data = client_socket.recv(1024)
                if data:
                    resposta = data.decode()
                    print(f'Resposta recebida: "{resposta}"')
                    incrementa_clock(peer)
                    resposta_partes = separar_msg(resposta)
                    resp_tipo = resposta_partes['tipo']
                    resp_args = resposta_partes['args']
                    atualiza_status_vizinho(peer, endereco_servidor, porta_servidor,'ONLINE')
                    if resp_tipo == 'PEER_LIST':
                        processa_peer_list(peer,resp_args)
                    return mensagem
            return mensagem
    except:
        if tipo == 'BYE':
            return True
        return atualiza_status_vizinho(peer, endereco_servidor, porta_servidor,'OFFLINE')

def start_client(peer=None):
    """
    Inicia o cliente P2P, exibindo um menu de opções para interação com a rede.
    """
    opcoes_validas = {
        1: lambda: listar_peers(peer),
        2: lambda: obter_peers(peer),
        3: lambda: listar_arquivos_locais(peer['diretorio_compartilhado']),
        4: buscar_arquivos,
        5: exibir_estatisticas,
        6: alterar_tamanho_chunk,
        9: lambda: sair(peer)
    }
    running = True
    while running:
        print("Escolha um tipo: ")
        print("\t[1] Listar peers")
        print("\t[2] Obter peers")
        print("\t[3] Listar arquivos locais")
        print("\t[4] Buscar arquivos")
        print("\t[5] Exibir estatisticas")
        print("\t[6] Alterar tamanho de chunk")
        print("\t[9] Sair")
        opcao = input()
        try:
            int_opcao = int(opcao)
            if int_opcao in opcoes_validas:
                running = opcoes_validas[int_opcao]()
            else:
                print("Opção inválida!")
        except ValueError:
            print("Entrada inválida! Digite um número.")

def listar_peers(peer):
    """
    Exibe a lista de vizinhos do peer e permite interagir com eles.
    """
    vizinhos = peer['vizinhos']
    while True:
        imprimir_lista_peers(vizinhos)
        opcao = input()
        try:
            int_opcao = int(opcao)
            if int_opcao == 0:
                return True
            elif 1 <= int_opcao <= len(vizinhos):
                vizinho = vizinhos[int_opcao - 1]
                send_menssage(peer, vizinho[0], vizinho[1], 'HELLO')
                return True
            else:
                print("Opção inválida!")
        except ValueError:
            print("Entrada inválida! Digite um número.")
            return False
        except IndexError:
            print("Erro: Lista de vizinhos mal formatada.")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False

def obter_peers(peer):
    """
    Solicita a lista de peers de todos os vizinhos conhecidos.
    """
    try:
        vizinhos = list(peer['vizinhos']) # Cria uma cópia da lista original
        for vizinho in vizinhos:
            send_menssage(peer, vizinho[0],vizinho[1] ,'GET_PEERS')
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def listar_arquivos_locais(diretorio_compartilhado):
    """
    Lista os arquivos presentes em um diretório compartilhado local.
    """
    try:
        for arquivo in os.listdir(diretorio_compartilhado):
            print(f"\t{arquivo}")
    except Exception as e:
        print(f"Erro {e} em '{diretorio_compartilhado}'.")
    return True

def buscar_arquivos():
    print("Buscar arquivos chamado")
    return True

def exibir_estatisticas():
    print("Exibir estatisticas chamado")
    return True

def alterar_tamanho_chunk():
    print("Alterar tamanho de chunk chamado")
    return True

def sair(peer):
    """
    Encerra a conexão do peer com o servidor e notifica os vizinhos sobre a saída.
    """
    print("Saindo...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((peer["endereco"], peer["porta"]))
        client_socket.sendall("SAIR".encode())
    for vizinho in peer['vizinhos']:
        send_menssage(peer,vizinho[0],vizinho[1],'BYE')
    return False

def imprimir_lista_peers(vizinhos):
    """
    Imprime a lista de vizinhos com seus respectivos endereços, portas e status.
    """
    print("Lista de peers:")
    print("\t[0] voltar para o menu anterior")
    for index, vizinho in enumerate(vizinhos, start=1):
        if len(vizinho) >= 3:
            print(f"\t[{index}] {vizinho[0]}:{vizinho[1]} {vizinho[2]}")
        else:
            print(f"\t[{index}] {vizinho[0]}:{vizinho[1]} (Status desconhecido)")

def processa_peer_list(peer,resp_args):
    """
    Processa a lista de vizinhos recebida do servidor e atualiza o status dos vizinhos no peer.
    Se o peer não existir atualiza_status_vizinho adiciona ele na lista de vizinhos e no arquivo
    """
    for vizinho in resp_args[1:]:
        vizinho_partes = vizinho.split(':')
        vizinho_endereco, vizinho_porta, vizinho_status, vizinho_zero = vizinho_partes
        vizinho_info = [vizinho_endereco, vizinho_porta]
        if vizinho_info[0] != peer['endereco'] or vizinho_info[1] != peer['porta']:
            atualiza_status_vizinho(peer, vizinho_endereco, vizinho_porta, vizinho_status)
