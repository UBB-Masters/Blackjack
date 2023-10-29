
import socket
import pickle


def game_client():
    server_ip = '127.0.0.1'
    server_port = 9999

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    # Receive game results from the server
    game_result = client.recv(1024)
    dealer_score, winning_players = pickle.loads(game_result)

    print("Dealer's Score:", dealer_score)
    print("Winning Players:", winning_players)

    client.close()


if __name__ == "__main__":
    game_client()
