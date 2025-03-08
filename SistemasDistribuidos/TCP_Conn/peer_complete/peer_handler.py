import os

connected_peers = {}  # Stores peer addresses and their status

def txt_to_str_list(filename):
    """Reads a text file and returns a list of stripped lines."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Warning: File '{filename}' not found. No peers loaded.")
        return []
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        return []

def load_peers_from_file(filename):
    """Initializes connected_peers with addresses from a file, setting them as OFFLINE."""
    global connected_peers
    peer_list = txt_to_str_list(filename)
    connected_peers = {peer: "OFFLINE" for peer in peer_list}

def handle_peer(peer_socket, addr):
    """Handles communication with a connected peer and updates status."""
    peer_address = f"{addr[0]}:{addr[1]}"
    
    # If it's a new peer, add it to the list with ONLINE status
    if peer_address not in connected_peers:
        connected_peers[peer_address] = "OFFLINE"
    
    connected_peers[peer_address] = "ONLINE"

    with peer_socket:
        while True:
            try:
                data = peer_socket.recv(1024)
                if not data:
                    break
                # Process received data (e.g., message parsing)
            except ConnectionResetError:
                break  # Handle unexpected disconnect

    connected_peers[peer_address] = "OFFLINE"

def get_connected_peers():
    """Returns a dictionary of peers and their statuses."""
    load_peers_from_file("neighbors.txt")
    return connected_peers.copy()
