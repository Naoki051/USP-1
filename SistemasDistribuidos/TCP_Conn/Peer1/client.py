import socket
import os

def cliente(data,index,tipo, args=""):
    """ Conecta-se a um servidor TCP e troca mensagens """
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    incrementa_clock(data)

    try:
        ip_vizinho = data['vizinhos'][index]['ip']
        port_vizinho = data['vizinhos'][index]['port']
        status_vizinho = data['vizinhos'][index]['status']

        mensagem = juntar_msg(data,tipo,args)
        print(f"Encaminhando mensagem \"{mensagem}\" para {ip_vizinho}:{port_vizinho}")

        cliente_socket.connect((ip_vizinho,port_vizinho))
        cliente_socket.send(mensagem.encode())
            
        if tipo.upper() == "HELLO":
            if status_vizinho != 'ONLINE':
                data['vizinhos'][index]['status'] = 'ONLINE'
                print(f"Atualizando peer {ip_vizinho}:{port_vizinho} status ONLINE")
        else:
            try:
                resposta = cliente_socket.recv(1024).decode()
                if resposta:
                    print(f"Resposta recebida: {resposta}")
                    if  status_vizinho != 'ONLINE':
                        data['vizinhos'][index]['status'] = 'ONLINE'
                        print(f"Atualizando peer {ip_vizinho}:{port_vizinho} status ONLINE")
                    resposta = separar_msg(resposta)
                    incrementa_clock(data,resposta['origem_clock'])

                    if resposta['tipo'] == 'PEER_LIST':
                        atualizar_vizinhos(data, resposta['args'])
            except Exception as e:
                print(f"Erro cliente ao receber resposta: {e}")
        
            

        cliente_socket.close()
    except Exception as e:
        if status_vizinho != 'OFFLINE':
            data['vizinhos'][index]['status'] = 'OFFLINE'
            print(f"Atualizando peer {ip_vizinho}:{port_vizinho} status ONLINE")

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
        argumentos = partes[3:]
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

def atualizar_vizinhos(data, mensagem):
    try:
        num_vizinhos = int(mensagem[0])
        vizinhos_str = mensagem[1:]

        for vizinho_str in vizinhos_str:
            if vizinho_str:
                ip, port, status, _ = vizinho_str.split(":")
                port = int(port)
                vizinho_encontrado = False
                for vizinho in data['vizinhos']:
                    if vizinho['ip'] == ip and vizinho['port'] == port:
                        if vizinho['status'] != status:
                            print(f"Atualizando peer {ip}:{port} status {status}")  # Print do vizinho encontrado
                            vizinho['status'] = status
                        vizinho_encontrado = True
                        break

                if not vizinho_encontrado:
                    novo_vizinho = {"ip": ip, "port": port, "status": status}
                    data['vizinhos'].append(novo_vizinho)
                    print(f"Adicionando novo peer {ip}:{port} status {status}")  # Print do vizinho adicionado
                    try:
                        with open("vizinhos.txt", "a") as arquivo:
                            arquivo.write(f"\n{ip}:{port}")
                    except Exception as e:
                        print(f"Erro ao adicionar vizinho ao arquivo: {e}")

    except ValueError:
        print(mensagem)
        print("Erro ao processar a mensagem de vizinhos.")
    except Exception as e:
        print(f"Erro inesperado: {e}")