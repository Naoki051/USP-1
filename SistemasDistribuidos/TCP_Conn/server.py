import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server started on {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Received: {data}")

                if data.strip().upper() == "OUT":
                    close_message = "Server closed successfully!"
                    conn.sendall(close_message.encode())  # Send close message
                    print("Shutdown request received. Closing server...")
                    break
                
                conn.sendall(data.encode())  # Echo back the message

if __name__ == "__main__":
    start_server()
