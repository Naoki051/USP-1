clock_counter = 0

def increment_clock(received_clock=None):
    """Updates the logical clock based on received messages."""
    global clock_counter
    if received_clock is not None:
        clock_counter = max(clock_counter, received_clock) + 1
    else:
        clock_counter += 1
    return clock_counter

def format_message(host, port, clock, msg_type, arguments=""):
    """Formats a message according to the protocol: 'HOST:PORT CLOCK TYPE ARGUMENTS'."""
    return f"{host}:{port} {clock} {msg_type} {arguments}".strip()


def parse_message(message):
    """Parses an incoming message."""
    parts = message.split(" ", 2)
    if len(parts) < 2:
        return None  # Invalid message format

    try:
        received_clock = int(parts[0])
    except ValueError:
        return None  # Invalid clock value

    msg_type = parts[1]
    arguments = parts[2] if len(parts) > 2 else ""

    return {
        "clock": received_clock,
        "type": msg_type,
        "arguments": arguments
    }
