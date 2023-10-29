import socket
import pickle
import threading

def handle_client(client):
    data = client.recv(1024)
    try:
        game_result = pickle.loads(data)
        # Process the game result received from the client
        print("Dealer's Score:", game_result[0])
        print("Winning Players:", game_result[1])
    except pickle.UnpicklingError as e:
        print("Error receiving and processing the game result:", e)

    client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(2)

    print("Server is waiting for player connections...")

    while True:
        client, addr = server.accept()
        print(f"Connected to {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

    server.close()

if __name__ == "__main__":
    main()
