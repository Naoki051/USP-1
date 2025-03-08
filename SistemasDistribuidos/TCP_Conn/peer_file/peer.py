import socket
import threading

HOST = '127.0.0.1'  # Peer IP
PORT = 65433        # Peer port
clock_counter = 0   # Logical clock
peers = {}          # Dictionary to track connected peers

def increment_clock(received_clock=None):
    """Updates the logical clock based on received messages."""
    global clock_counter
    if received_clock is not None:
        clock_counter = max(clock_counter, received_clock) + 1
    else:
        clock_counter += 1
    return clock_counter

def format_message(host, port, clock, msg_type, arguments=""):
    """Formats a message according to the protocol."""
    return f"{host}:{port} {clock} {msg_type} {arguments}".strip()

def parse_message(message):
    """Parses an incoming message."""
    parts = message.split(" ", 3)
    if len(parts) < 3:
        return None  # Invalid message format

    host_port = parts[0]
    try:
        received_clock = int(parts[1])
    except ValueError:
        return None  # Invalid clock value

    msg_type = parts[2]
    arguments = parts[3] if len(parts) > 3 else ""

    return {
        "host_port": host_port,
        "clock": received_clock,
        "type": msg_type,
        "arguments": arguments
    }

def handle_peer(peer_socket, addr):
    """Handles communication with a connected peer."""
    global clock_counter
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
                print(f"Received: {parsed_message}, Updated Clock: {clock_counter}")

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

def peer_server():
    """Starts the peer's server to accept connections from other peers."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Peer listening on {HOST}:{PORT}")

        while True:
            peer_socket, addr = server_socket.accept()
            threading.Thread(target=handle_peer, args=(peer_socket, addr), daemon=True).start()

def connect_to_peer(peer_ip, peer_port, msg_type, arguments=""):
    """Connects to another peer, sends a message, and waits for a response."""
    global clock_counter

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((peer_ip, peer_port))

            # Increment clock before sending
            message = format_message(HOST, PORT, increment_clock(), msg_type, arguments)
            client_socket.sendall(message.encode())

            if msg_type.strip().upper() == "OUT":
                print("Sent shutdown signal. Disconnecting...")

        except ConnectionRefusedError:
            print("Unable to connect. Ensure the peer is running.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Start the peer's server in a separate thread
    threading.Thread(target=peer_server, daemon=True).start()

    while True:
        command = input("Enter 'connect' to send a message, or 'exit' to stop the peer: ").strip().lower()
        if command == "connect":
            peer_ip = input("Enter peer IP: ").strip()
            peer_port = int(input("Enter peer port: ").strip())
            msg_type = input("Enter message type (e.g., PING, OUT): ").strip()
            arguments = input("Enter arguments (or leave empty): ").strip()

            connect_to_peer(peer_ip, peer_port, msg_type, arguments)

        elif command == "exit":
            print("Shutting down peer...")
            break
