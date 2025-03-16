import socket
import os

def cliente(data,index,tipo, args=""):
    """ Conecta-se a um servidor TCP e troca mensagens """
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect((data['vizinhos'][index]['ip'],data['vizinhos'][index]['port']))
        print(f"Conectado ao servidor {data['vizinhos'][index]['ip']}:{data['vizinhos'][index]['port']}")

        mensagem = juntar_msg(data,tipo,args)
        incrementa_clock(data)
        cliente_socket.send(mensagem.encode())
        

        if tipo.upper() == "SAIR":
            print("Encerrando conexão cliente...")
            
        if tipo == 'HELLO':
            if data['vizinhos'][index]['status'] != 'ONLINE':
                data['vizinhos'][index]['status'] = 'ONLINE'
                print(f"Status {data['vizinhos'][index]['ip']}:{data['vizinhos'][index]['port']} atualizado para ONLINE")
        else:
            try:
                resposta = cliente_socket.recv(1024).decode()
                print(f"Recebeu: {resposta}")
                resposta = separar_msg(resposta)
                incrementa_clock(data,resposta['origem_clock'])
            except Exception as e:
                print(f"Erro ao receber resposta: {e}")
            

        cliente_socket.close()
    except Exception as e:
        print(f"Erro ao conectar com {data['vizinhos'][index]['ip']}:{data['vizinhos'][index]['port']}: {e}")
        if data['vizinhos'][index]['status'] != 'OFFLINE':
            data['vizinhos'][index]['status'] = 'OFFLINE'
            print(f"Status {data['vizinhos'][index]['ip']}:{data['vizinhos'][index]['port']} atualizado para OFFLINE")

def dict_vizinhos(nome_arquivo='vizinhos.txt'):
    vizinho = []
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    ip, port = linha.split(':')
                    vizinho.append({
                        'ip': ip,
                        'port': int(port),
                        'status': 'OFFLINE'
                    })
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    return vizinho

def juntar_msg(data,tipo,args=""):
    mensagem = f"{data['ip']}:{data['port']} {data['clock']} {tipo} {args}"
    return mensagem

def separar_msg(mensagem):
    partes = mensagem.split(" ")
    origem = partes[0].split(":")
    origem_ip = origem[0]
    origem_port = int(origem[1])
    origem_clock = int(partes[1])
    mensagem_tipo = partes[2]

    if len(partes) > 3: #argumentos opcionais existem        
        argumentos = partes[3]
    else: #argumentos opcionais não existem
        argumentos = None

    mensagem = {
        "origem_ip": origem_ip,
        "origem_port": origem_port,
        "origem_clock": origem_clock,
        "tipo": mensagem_tipo,
        "args": argumentos
    }

    return mensagem

def incrementa_clock(data,msg_clock=0):
    data["clock"] = max(data["clock"], msg_clock) + 1
    print(f'Relógio atualizado para {data["clock"]}') 
    return

def listar_vizinhos(data):
    print("Lista de peers: ")
    print("[0] voltar para o menu anterior")
    for i,vizinho in enumerate(data['vizinhos'],1):
        print(f"[{i}] {vizinho['ip']}:{vizinho['port']} {vizinho['status']}")

def listar_arquivos(data):
    try:
        arquivos = os.listdir(data['files_path'])
        for arquivo in arquivos:
            print(arquivo)
    except FileNotFoundError:
        print(f"Erro: O diretório '{data['files_path']}' não foi encontrado.")
