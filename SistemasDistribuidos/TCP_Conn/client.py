import socket
import threading

HOST = '127.0.0.1'  # Server's hostname or IP
PORT = 65432        # Port to connect to

clock_counter = 0  # Logical clock for event ordering
shutdown_flag = threading.Event()

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

def peer_client(target_ip, target_port):
    """Connects to another peer and sends messages while maintaining logical clock."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((target_ip, target_port))

        while True:
            msg_type = input("Enter message type (or 'OUT' to disconnect): ")
            arguments = input("Enter arguments (or leave empty): ")

            message = format_message(HOST, PORT, increment_clock(), msg_type, arguments)
            client_socket.sendall(message.encode())

            if msg_type.strip().upper() == "OUT":
                print("Sent shutdown signal. Closing peer.")
                shutdown_flag.set()
                break


if __name__ == "__main__":

    target_ip = input("Enter peer IP to connect to: ")
    target_port = int(input("Enter peer port: "))

    peer_client(target_ip,target_port)
