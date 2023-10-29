
import socket
import pickle
import threading
from BlackjackServer.BlackJack.black_jack_game import Blackjack, Player, Dealer, Deck



def handle_client(client):
    # Initialize the game for the client
    num_players = 2
    players = [Player(input(f"Player {i}, say your name: ")) for i in range(1, num_players + 1)]
    game = Blackjack(players)

    dealer_score, winning_players = game.play_game()

    game_result = (dealer_score, [player.name for player in winning_players])
    client.send(pickle.dumps(game_result))  # Send game results to the client
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
