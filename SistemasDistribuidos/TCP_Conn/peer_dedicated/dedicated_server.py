import socket
import threading

HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server port
clock_counter = 0   # Logical clock
clients = {}        # Dictionary to store client sockets and addresses

def increment_clock(received_clock=None):
    """Updates the logical clock based on received messages."""
    global clock_counter
    if received_clock is not None:
        clock_counter = max(clock_counter, received_clock) + 1
    else:
        clock_counter += 1
    return clock_counter

def broadcast_message(message, sender_socket):
    """Sends a message to all connected clients except the sender."""
    for client_socket in list(clients.keys()):
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode())
            except:
                print(f"Removing disconnected client: {clients[client_socket]}")
                remove_client(client_socket)

def remove_client(client_socket):
    """Removes a client from the list and closes the socket."""
    if client_socket in clients:
        print(f"Closing connection with {clients[client_socket]}")
        client_socket.close()
        del clients[client_socket]

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

def handle_client(client_socket, addr):
    """Handles communication with a single client."""
    global clock_counter
    print(f"New connection from {addr}")
    clients[client_socket] = addr

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break  # Peer disconnected

            parsed_message = parse_message(data)
            if parsed_message:
                increment_clock(parsed_message["clock"])
                print(f"Received: {parsed_message}")

                if parsed_message["type"] == "OUT":
                    print(f"Peer {addr} requested to disconnect.")
                    client_socket.sendall("Peer disconnected successfully!".encode())
                    break

    except (ConnectionResetError, BrokenPipeError):
        print(f"Peer {addr} disconnected unexpectedly.")

    finally:
        remove_client(client_socket)

def server():
    """Main server function to handle multiple clients."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    server()
