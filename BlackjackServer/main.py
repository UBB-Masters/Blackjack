import socket

from black_jack_game import BlackjackGame


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

    # Create an instance of the BlackjackGame class
    blackjack_game = BlackjackGame()

    # Start the game
    blackjack_game.start_game()

    # Start the game
    blackjack_game.start_game()

    # Start the game
    blackjack_game.start_game()
    while not blackjack_game.check_game_over():
        for addr, player in connected_clients.items():
            game_state = blackjack_game.get_game_state()

            # Wait for the current player's action
            action = player.recv(1024).decode()
            # Process the player's action and update the game state
            blackjack_game.player_action(action)

            # Send the game state to both players after a player's action
            for player in connected_clients.values():
                player.send(str(game_state).encode())

        # Check if the game is over after each player's action
        if blackjack_game.is_game_over():
            break

    # Determine the game result when the game is over
    game_results = blackjack_game.determine_game_result()
    for addr, player in connected_clients.items():
        player_index = list(connected_clients.keys()).index(addr)
        result_message = f"Game Result: {game_results[player_index]}"
        player.send(result_message.encode())

    # Close the server when the game is finished
    server.close()


main()