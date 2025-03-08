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

if __name__ == "__main__":
    peer_id = 2
    host = '127.0.0.1'
    port = 9001

    servidor(peer_id, host,port)

