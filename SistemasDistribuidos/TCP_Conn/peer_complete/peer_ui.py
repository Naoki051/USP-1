import threading
from peer_server import start_peer_server, shutdown_server
from peer_handler import get_connected_peers

def display_menu():
    """Displays the menu options for the peer."""
    print("\nPeer-to-Peer Network Menu")
    print("[1] List Peers")
    print("[0] Exit")

def display_peers():
    """Displays the list of peers with their statuses."""
    peers = get_connected_peers()

    print("\n[1] Return to menu")
    if not peers:
        print("No peers currently connected.")
        return

    for index, (peer, status) in enumerate(peers.items(), start=2):
        print(f"[{index}] {peer} {status}")

def handle_user_input():
    """Handles user input and performs actions based on the selected option."""
    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            display_peers()
        elif choice == "0":
            print("Shutting down peer...")
            shutdown_server()
            break
        else:
            print("Invalid option. Please select again.")

if __name__ == "__main__":
    # Start the peer server in a background thread
    threading.Thread(target=start_peer_server, daemon=True).start()

    # Run the menu interface
    handle_user_input()
