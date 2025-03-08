import socket

SERVER_IP = '127.0.0.1'  # Dedicated server or peer IP
SERVER_PORT = 65432       # Dedicated server or peer port
clock_counter = 0         # Logical clock

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

def send_message(msg_type, arguments=""):
    """Sends a single message to the server and waits for a response."""
    global SERVER_IP, SERVER_PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((SERVER_IP, SERVER_PORT))

            # Increment clock before sending
            message = format_message(SERVER_IP, SERVER_PORT, increment_clock(), msg_type, arguments)
            client_socket.sendall(message.encode())

            if msg_type.strip().upper() == "OUT":
                print("Sent shutdown signal. Disconnecting...")

        except ConnectionRefusedError:
            print("Unable to connect. Ensure the server is running.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    msg_type = input("Enter message type (e.g., PING, OUT): ").strip()
    arguments = input("Enter arguments (or leave empty): ").strip()
    
    send_message(msg_type, arguments)
