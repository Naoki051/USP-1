import socket
def cliente(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host,port))
            msg = input(f"Enviar: ")
            client_socket.send(msg.encode())
            print(f"Message sent to {host}:{port}: {msg}")
        except Exception as e:
            print(f"Erro: {e}")

host = "127.0.0.1"
port = 9000

cliente(host,port)