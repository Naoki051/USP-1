import socket
from utils import increment_clock, format_message
from peer_server import HOST, PORT

sender_ip = HOST
sender_port = PORT

def connect_to_peer(peer_ip, peer_port, sender_ip, sender_port, msg_type, arguments=""):
    """Connects to another peer and sends a message without waiting for a response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((peer_ip, peer_port))

            # Format message with sender address
            message = format_message(sender_ip, sender_port, increment_clock(), msg_type, arguments)
            client_socket.sendall(message.encode())

            print(f"Message sent to {peer_ip}:{peer_port}: {message}")

        except ConnectionRefusedError:
            print("Unable to connect. Ensure the peer is running.")
        except Exception as e:
            print(f"Error: {e}")
