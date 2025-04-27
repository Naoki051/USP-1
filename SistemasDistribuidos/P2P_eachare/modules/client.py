import socket,os,base64
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
            elif tipo == 'LS':
                data = client_socket.recv(1024)
                if data:
                    resposta = data.decode()
                    print(f'Resposta recebida: "{resposta}"')
                    incrementa_clock(peer)
                    resposta_partes = separar_msg(resposta)
                    resp_tipo = resposta_partes['tipo']
                    resp_args = resposta_partes['args']
                    atualiza_status_vizinho(peer, endereco_servidor, porta_servidor,'ONLINE')
                    if resp_tipo == 'LS_LIST':
                        return processar_ls_list(resp_args,endereco_servidor, porta_servidor)
            elif tipo == 'DL':
                data = client_socket.recv(1024)
                if data:
                    resposta = data.decode()
                    print(f'Resposta recebida: \"{(resposta[:97] + '...') if len(resposta) > 100 else resposta}\""')
                    incrementa_clock(peer)
                    resposta_partes = separar_msg(resposta)
                    resp_tipo = resposta_partes['tipo']
                    resp_args = resposta_partes['args']
                    atualiza_status_vizinho(peer, endereco_servidor, porta_servidor,'ONLINE')
                    if resp_tipo == 'FILE':
                        try:
                            caminho_arquivo = f"arquivos/{resp_args[0]}"
                            string_base64 = base64.b64decode(resp_args[3]).decode('utf-8')
                            with open(caminho_arquivo, 'w') as arquivo:
                                arquivo.write(string_base64)
                            print(f"Download do arquivo {resp_args[0]} finalizado.")
                        except Exception as e:
                            print(f"Erro ao receber ou salvar o arquivo de {endereco_servidor}: {e}")
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
        4: lambda: buscar_arquivos(peer),
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
            print(f"Erro inesperado listar_peers: {e}")
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
        print(f"Erro obter_peers: {e}")
        return False

def listar_arquivos_locais(diretorio_compartilhado):
    """
    Lista os arquivos presentes em um diretório compartilhado local.
    """
    try:
        for arquivo in os.listdir(diretorio_compartilhado):
            print(f"\t{arquivo}")
    except Exception as e:
        print(f"Erro listar_arquivos_locais {e} em '{diretorio_compartilhado}'.")
    return True

def buscar_arquivos(peer):
    try:
        arquivos_encontrados=[]
        for vizinho in peer['vizinhos']:
            if vizinho[2] == 'ONLINE':
                arquivos_vizinho = send_menssage(peer,vizinho[0],vizinho[1],'LS')
                arquivos_encontrados.extend(arquivos_vizinho)
        
        lista_arquivos = exibir_arquivos_encontrados(arquivos_encontrados)
        for item in lista_arquivos:    
            print(item,":", lista_arquivos[item])
        requisitar_download_com_cancelar(lista_arquivos,peer)
        return True
    except Exception as e:
        print(f"Erro buscar_arquivos: {e}")
        return False

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
            atualiza_status_vizinho(peer, vizinho_endereco, vizinho_porta, vizinho_status,resp_args[0])

def processar_ls_list(resp_args,endereco_origem,porta_origem):
    """
    Processa a parte da lista de arquivos da mensagem de resposta LS_LIST e
    retorna uma lista de dicionários com as informações dos arquivos e o peer.
    """
    arquivos_str = resp_args[1:]  # Pega a lista de strings "nome:tamanho"
    peer_endereco_porta = f"{endereco_origem}:{porta_origem}"
    arquivos_data = []
    for arquivo_info_str in arquivos_str:
        partes_arquivo = arquivo_info_str.split(':')
        if len(partes_arquivo) >= 1:
            nome_arquivo = partes_arquivo[0]
            tamanho = int(partes_arquivo[1]) if len(partes_arquivo) > 1 and partes_arquivo[1].isdigit() else 0
            arquivos_data.append({'nome': nome_arquivo, 'tamanho': tamanho, 'peer': peer_endereco_porta})
        else:
            print(f"Erro: Formato inválido na informação do arquivo: {arquivo_info_str}")
    return arquivos_data

def exibir_arquivos_encontrados(lista_de_arquivos):
    """
    Exibe a lista de arquivos encontrados na rede e retorna um dicionário
    mapeando o número da opção ao dicionário do arquivo.

    Args:
        lista_de_arquivos: Uma lista de dicionários, onde cada dicionário contém
                           'nome', 'tamanho' e 'peer'.

    Returns:
        dict: Um dicionário onde as chaves são os números das opções (strings)
              e os valores são os dicionários de arquivos correspondentes.
              Inclui a opção '0' para cancelar com valor None.
    """
    arquivos_dict = {}
    print("Arquivos encontrados na rede:")
    print("{:^5} | {:<16} | {:<9} | {:<17}".format("Num", "Nome", "Tamanho", "Peer"))
    print("-" * 5 + "-|-" + "-" * 16 + "-|-" + "-" * 9 + "-|-" + "-" * 17)
    print("{:^5} | {:<16} | {:<9} | {:<17}".format("[ 0]", "<Cancelar>", "", ""))
    for i, arquivo in enumerate(lista_de_arquivos):
        nome = arquivo.get('nome', '')
        tamanho = arquivo.get('tamanho', '')
        peer = arquivo.get('peer', '')
        opcao = f"[{i+1:2}]"
        print("{:^5} | {:<16} | {:<9} | {:<17}".format(opcao, nome, str(tamanho), peer))
        arquivos_dict[str(i + 1)] = arquivo
    return arquivos_dict

def requisitar_download_com_cancelar(lista_de_arquivos, peer_atual):
    """
    Permite ao usuário escolher um arquivo da lista (ou cancelar) e envia uma
    mensagem DL para o peer que possui o arquivo.

    Args:
        lista_de_arquivos: Lista de dicionários com informações dos arquivos.
        peer_atual: Dicionário representando o peer atual.
    """
    while True:
        try:
            escolha = input("Digite o numero do arquivo para fazer o download (ou 0 para cancelar): ")
            numero_escolhido = int(escolha)
            if numero_escolhido == 0:
                print("Download cancelado.")
                return None  # Indica que o download foi cancelado
            elif 1 <= numero_escolhido <= len(lista_de_arquivos):
                arquivo_selecionado = lista_de_arquivos.get(f'{numero_escolhido}','')
                print("arquivo_selecionado:",arquivo_selecionado)
                nome_arquivo = arquivo_selecionado.get('nome', '')
                peer_arquivo_str = arquivo_selecionado.get('peer', '')
                peer_arquivo = peer_arquivo_str.split(':')
                print("peer_arquivo:",peer_arquivo)
                if len(peer_arquivo) == 2:
                    endereco_peer_arquivo = peer_arquivo[0]
                    porta_peer_arquivo = int(peer_arquivo[1])
                    args_dl = f"{nome_arquivo} 0 0"
                    send_menssage(peer_atual, endereco_peer_arquivo, porta_peer_arquivo, 'DL', args_dl)
                    
                    return arquivo_selecionado  # Retorna o arquivo selecionado
                else:
                    print(f"Formato inválido para o peer do arquivo: {peer_arquivo_str}")
                    return None
            else:
                print("Numero de arquivo inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um numero.")
        except Exception as e:
            print(f"Erro em requisitar_download_com_cancelar: {e}")
            return None
