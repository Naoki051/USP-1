import socket
def cliente(peer_id,host,port):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host,port))
        while True:
            msg = input(f"{peer_id}: ")
            cliente_socket.send(msg.encode())

            resposta = cliente_socket.recv(1024).decode()
            print(f"resposta: {resposta}")
    except Exception as e:
        print(f"Erro: {e}")

