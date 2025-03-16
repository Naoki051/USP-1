import socket
from client import separar_msg,incrementa_clock

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
                        resposta = f"{data['ip']}:{data['port']} {data['clock']} PEER_LIST {len(data['vizinhos'])} "
                        for vizinho in data['vizinhos']:
                            resposta += f"{vizinho['ip']}:{vizinho['port']}:{vizinho['status']}:0 "
                        incrementa_clock(data)
                        conexao.send(resposta.encode())
                except Exception as e:
                    print(f"Erro na conexão: {e}")
                
    print(f"Servidor finalizado.")

data = {
    "ip": "127.0.0.1",
    "port": 9009,
    "clock": 0,
    "files_path":'./arquivos',
    'vizinhos': []
}

servidor(data)