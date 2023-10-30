# # import socket
# # import pickle
# # from BlackjackServer.BlackJack.black_jack_game import Blackjack, Player
# #
# # def game_client():
# #     server_ip = '127.0.0.1'
# #     server_port = 9999
# #
# #     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client.connect((server_ip, server_port))
# #
# #     player_names = [input(f"Player {i}, say your name: ") for i in range(1, 3)]
# #     players = [Player(name) for name in player_names]
# #     game = Blackjack(players)
# #
# #     dealer_score, winning_players = game.play_game()
# #     game_result = (dealer_score, [player.name for player in winning_players])
# #
# #     client.send(pickle.dumps(game_result))  # Send game results to the server
# #     client.close()
# #
# # if __name__ == "__main__":
# #     game_client()
# #
# import socket
# import pickle
# from BlackjackServer.BlackJack.black_jack_game import Blackjack, Player
#
# def game_client():
#     # server_ip = '10.152.4.197'  # Replace with the IP address of the server
#     server_ip = '127.0.0.1'  # Replace with the IP address of the server
#     server_port = 9999  # The same port as the server
#
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, server_port))
#
#     player_id = client.recv(1024).decode()  # Receive the assigned player ID
#     print(f"You are {player_id}")
#
#     if player_id == "Player 1":
#         # Initialize the game for Player 1
#         player_names = [input("Player 1, say your name: ")]
#         players = [Player(name) for name in player_names]
#         game = Blackjack(players)
#
#         dealer_score, winning_players = game.play_game()
#         game_result = (dealer_score, [player.name for player in winning_players])
#
#         client.send(pickle.dumps(game_result))  # Send game results to the server
#         client.close()
#     elif player_id == "Player 2":
#         # Initialize the game for Player 2
#         player_names = [input("Player 2, say your name: ")]
#         players = [Player(name) for name in player_names]
#         game = Blackjack(players)
#
#         dealer_score, winning_players = game.play_game()
#         game_result = (dealer_score, [player.name for player in winning_players])
#
#         client.send(pickle.dumps(game_result))  # Send game results to the server
#         client.close()
#     else:
#         print("You are a spectator")
#
# if __name__ == "__main__":
#     game_client()
import socket
from BlackjackServer.BlackJack.black_jack_game import Blackjack, Player

def game_client(player_number):
    if player_number == 1:
        player_name = input("Player 1, say your name: ")
    elif player_number == 2:
        player_name = input("Player 2, say your name: ")
    else:
        print("Invalid player number.")
        return

    # Initialize the game for the player
    player_names = [player_name]
    players = [Player(name) for name in player_names]
    game = Blackjack(players)

    dealer_score, winning_players = game.play_game()
    game_result = f"Dealer's Score: {dealer_score}, Winning Players: {[player.name for player in winning_players]}"

    send_data_to_server(f"Player {player_number}", game_result)

def send_data_to_server(player_id, game_result):
    server_ip = '127.0.0.1'  # Replace with the IP address of the server
    server_port = 9999  # The same port as the server

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    data_to_send = player_id + '\n' + game_result  # Concatenating data
    client.sendall(data_to_send.encode())  # Send the combined data to the server

    client.close()

if __name__ == "__main__":
    player_number = int(input("Enter the player number (1 or 2): "))
    game_client(player_number)

