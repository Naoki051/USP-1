import socket
import os
from modules.utils import incrementa_clock, atualiza_status_vizinho,separar_msg
def cliente(peer, endereco, porta, tipo, args=''):
    try:
        incrementa_clock(peer)
        mensagem = f"{peer['endereco']}:{peer['porta']} {peer['clock']} {tipo} {args}".strip()
        mensagem+=f" para {endereco}:{porta}"
        print(f'Encaminhando mensagem: "{mensagem}"')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((endereco, porta))
            client_socket.send(mensagem.encode())
            if tipo == 'HELLO':
                atualiza_status_vizinho(peer,endereco,porta,"ONLINE")
            if tipo == 'GET_PEERS':
                atualiza_status_vizinho(peer,endereco,porta,"ONLINE")
            resp = client_socket.recv(1024)
            if resp:
                resp = resp.decode()
                print(f'Resposta recebida: "{resp}"')
                incrementa_clock(peer)
                resposta = separar_msg(resp)
                if resposta['tipo'] == 'PEER_LIST':
                    processa_peer_list(peer,resposta)
    except Exception as e:
        print(f'EXCEPTION:{e}' )
        atualiza_status_vizinho(peer, endereco, porta,"OFFLINE")

def imprimir_lista_peers(vizinhos):
    print("Lista de peers:")
    print("\t[0] voltar para o menu anterior")
    for index, vizinho in enumerate(vizinhos, start=1):
        if len(vizinho) >= 3:
            print(f"\t[{index}] {vizinho[0]}:{vizinho[1]} {vizinho[2]}")
        else:
            print(f"\t[{index}] {vizinho[0]}:{vizinho[1]} (Status desconhecido)")

def listar_peers(peer):
    vizinhos = peer['vizinhos']
    while True:
        imprimir_lista_peers(vizinhos)
        opcao = input()
        try:
            int_opcao = int(opcao)
            if int_opcao == 0:
                break
            elif int_opcao <= len(vizinhos):
                cliente(peer, vizinhos[int_opcao-1][0],vizinhos[int_opcao-1][1] ,'HELLO')
                break
            else:
                print("Opção inválida!")
        except ValueError:
            print("Entrada inválida! Digite um número.")
        except IndexError:
            print("Erro: Lista de vizinhos mal formatada.")
    
def adiciona_vizinho(peer,vizinho):
    peer['vizinhos'].append(vizinho)
    try:
        vizinho_str = ':'.join(vizinho[0:1])
        arquivo_vizinhos = peer['vizinhos_file']
        with open(arquivo_vizinhos, 'a') as arquivo:
            arquivo.write(vizinho_str)
        print(f"Adicionando novo peer {vizinho[0]}:{vizinho[1]} status {vizinho[2]}")
    except Exception as e:
        print(f"Erro ao salvar vizinho em {arquivo_vizinhos}: {e}")

def obter_peers(peer):
    vizinhos = peer['vizinhos']
    for vizinho in vizinhos:
        cliente(peer, vizinho[0],vizinho[1] ,'GET_PEERS')

def processa_peer_list(peer,mensagem):
    args_partes = mensagem['args'].split(' ')
    for vizinho in args_partes[1:]:
        vizinho_partes = vizinho.split(':')
        vizinho_endereco, vizinho_porta, vizinho_status, vizinho_zero = vizinho_partes
        vizinho_info = [vizinho_endereco, vizinho_porta, vizinho_status]
        if vizinho_info not in peer['vizinhos']:
            adiciona_vizinho(peer,vizinho_info)
        if vizinho_info[0] != peer['endereco'] and vizinho_info[1] != peer['porta']:
            atualiza_status_vizinho(peer,vizinho_endereco,vizinho_porta,vizinho_status)

def listar_arquivos_locais(diretorio_compartilhado):
    try:
        for arquivo in os.listdir(diretorio_compartilhado):
            print(f"\t{arquivo}")
    except Exception as e:
        print(f"Erro {e} em '{diretorio_compartilhado}'.")

def buscar_arquivos():
    print("Buscando arquivos...")
    # Adicione aqui a lógica para buscar arquivos

def exibir_estatisticas():
    print("Exibindo estatísticas...")
    # Adicione aqui a lógica para exibir estatísticas

def alterar_tamanho_chunk():
    print("Alterando tamanho de chunk...")
    # Adicione aqui a lógica para alterar o tamanho de chunk

def menu(peer):
    opcoes_validas = {
        1: lambda: listar_peers(peer),
        2: lambda: obter_peers(peer),
        3: listar_arquivos_locais,
        4: buscar_arquivos,
        5: exibir_estatisticas,
        6: alterar_tamanho_chunk
    }
    while True:
        print("Escolha um comando: ")
        print("\t[1] Listar peers")
        print("\t[2] Obter peers")
        print("\t[3] Listar arquivos locais")
        print("\t[4] Buscar arquivos")
        print("\t[5] Exibir estatisticas")
        print("\t[6] Alterar tamanho de chunk")
        print("\t[9] Sair")
        opcao =  input()
        try:
            int_opcao = int(opcao)
            if int_opcao == 9:
                print("Saindo...")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    try:
                        client_socket.connect((peer["endereco"], peer["porta"]))
                        mensagem = "SAIR"
                        client_socket.send(mensagem.encode())
                        for vizinho in peer['vizinhos']:
                            cliente(peer,vizinho[0],vizinho[1],"BYE")
                        break
                    except socket.error as e:
                        print(f"Erro ao conectar ou enviar: {e}")
                        break #sai do loop caso ocorra um erro.
            elif int_opcao in opcoes_validas:
                opcoes_validas[int_opcao]()
            else:
                print("Opção inválida!")
        except ValueError:
            print("Entrada inválida! Digite um número.")
