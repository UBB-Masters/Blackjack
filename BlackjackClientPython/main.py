import socket
import pickle
from BlackjackServer.BlackJack.black_jack_game import Blackjack, Player

def game_client():
    server_ip = '127.0.0.1'
    server_port = 9999

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    player_names = [input(f"Player {i}, say your name: ") for i in range(1, 3)]
    players = [Player(name) for name in player_names]
    game = Blackjack(players)

    dealer_score, winning_players = game.play_game()
    game_result = (dealer_score, [player.name for player in winning_players])

    client.send(pickle.dumps(game_result))  # Send game results to the server
    client.close()

if __name__ == "__main__":
    game_client()

