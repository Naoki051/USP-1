import socket
import threading
from peer_handler import handle_peer

HOST = '127.0.0.1'
PORT = 65431

def start_peer_server():
    """Starts the peer's server to accept connections from other peers."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Peer server listening on {HOST}:{PORT}")

        while True:
            peer_socket, addr = server_socket.accept()
            threading.Thread(target=handle_peer, args=(peer_socket, addr), daemon=True).start()
