import threading
from peer_server import start_peer_server
from peer_client import connect_to_peer

from peer_server import HOST, PORT

sender_ip = HOST
sender_port = PORT

if __name__ == "__main__":
    threading.Thread(target=start_peer_server, daemon=True).start()

    while True:
        command = input("Enter 'connect' to send a message, or 'exit' to stop the peer: ").strip().lower()
        if command == "connect":
            peer_ip = input("Enter peer IP: ").strip()
            peer_port = int(input("Enter peer port: ").strip())
            msg_type = input("Enter message type (e.g., PING, OUT): ").strip()
            arguments = input("Enter arguments (or leave empty): ").strip()

            connect_to_peer(peer_ip, peer_port,sender_ip,sender_port, msg_type, arguments)

        elif command == "exit":
            print("Shutting down peer...")
            break
