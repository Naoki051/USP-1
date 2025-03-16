import socket
import threading

def cliente(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host,port))
            msg = input(f"Enviar: ")
            client_socket.send(msg.encode())
            print(f"Message sent to {host}:{port}: {msg}")
        except Exception as e:
            print(f"Erro: {e}")

def servidor(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host,port))
        server_socket.listen(1)
        print(f"Esperando conn na port {port}." )

        while True:
                peer_socket, addr = server_socket.accept()
                threading.Thread(target=handle_peer, args=(peer_socket, addr), daemon=True).start()

peers = {}
clock_counter = 0

def increment_clock(received_clock=None):
    """Updates the logical clock based on received messages."""
    global clock_counter
    if received_clock is not None:
        clock_counter = max(clock_counter, received_clock) + 1
    else:
        clock_counter += 1
    return clock_counter

def parse_message(host,port,message):
    """Parses an incoming message."""
    parts = message.split(" ", 2)
    if len(parts) < 3:
        return None  # Invalid message format
    try:
        received_clock = int(parts[1])
    except ValueError:
        return None  # Invalid clock value

    host_port = f"{host}:{port}"
    msg_type = parts[2]
    arguments = parts[3] if len(parts) > 2 else ""

    return {
        "host_port": host_port,
        "clock": received_clock,
        "type": msg_type,
        "arguments": arguments
    }


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



host = "127.0.0.1"
port = 9000

servidor(host, port)