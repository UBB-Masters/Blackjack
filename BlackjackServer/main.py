import socket


def main():
    # Initialize the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(2)  # Listen for two clients

    print("Server is waiting for player connections...")

    # Keep track of connected players and their "ping" status
    connected_clients = {}

    while len(connected_clients) < 2:
        # Wait for a client to connect
        client, addr = server.accept()
        print(f"Connected to {addr}")

        # Implement a handshake mechanism
        data = client.recv(1024).decode()
        if data == "ping" and addr not in connected_clients:
            print("Received ping from client. Sending pong...")
            client.send("pong".encode())
            connected_clients[addr] = client

    # Both players are connected; the game can start
    print("Both players are connected. Starting the game...")

main()