import socket

def servidor(peer_id, host, port):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host,port))
    while True:
        servidor_socket.listen(1)
        print(f"{peer_id} esperando conn na port {port}." )

        conn, addr = servidor_socket.accept()
        msg = conn.recv(1024).decode()
        print(f"mensagem: {msg}")

