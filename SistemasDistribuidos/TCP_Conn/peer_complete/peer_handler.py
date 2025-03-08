import socket
from utils import increment_clock, parse_message

peers = {}

def handle_peer(peer_socket, addr):
    """Handles communication with a connected peer."""
    print(f"Connected to peer {addr}")
    peers[peer_socket] = addr

    try:
        while True:
            data = peer_socket.recv(1024).decode()
            if not data:
                break  # Peer disconnected

            parsed_message = parse_message(data)
            if parsed_message:
                increment_clock(parsed_message["clock"])
                print(f"Received: {parsed_message}")

                if parsed_message["type"] == "OUT":
                    print(f"Peer {addr} requested to disconnect.")
                    peer_socket.sendall("Peer disconnected successfully!".encode())
                    break

    except (ConnectionResetError, BrokenPipeError):
        print(f"Peer {addr} disconnected unexpectedly.")

    finally:
        remove_peer(peer_socket)

def remove_peer(peer_socket):
    """Removes a disconnected peer from the list."""
    if peer_socket in peers:
        print(f"Closing connection with {peers[peer_socket]}")
        peer_socket.close()
        del peers[peer_socket]
