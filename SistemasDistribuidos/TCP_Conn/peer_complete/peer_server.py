import socket
import threading
from peer_handler import handle_peer

HOST = "127.0.0.1"
PORT = 65432

server_socket = None  # Reference for shutting down the server

def start_peer_server():
    """Starts the peer server to accept connections from other peers."""
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Peer server listening on {HOST}:{PORT}")

    while True:
        try:
            peer_socket, addr = server_socket.accept()
            threading.Thread(target=handle_peer, args=(peer_socket, addr), daemon=True).start()
        except OSError:
            break  # Exit gracefully when shutting down

def shutdown_server():
    """Gracefully shuts down the server."""
    global server_socket
    if server_socket:
        server_socket.close()
