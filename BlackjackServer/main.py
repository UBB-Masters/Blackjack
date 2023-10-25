import socket
import threading

# Define constants for card values
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Define a deck of cards
deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4

# Initialize the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(2)  # Allows two players to connect

# Store connected players and their game states
players = []
player_states = {}

# Initialize the game state
game_state = {
    'deck': deck,
    'dealer_hand': [],
    'player_turn': 0  # Index of the player taking the current turn
}


def deal_initial_cards():
    """Deal two cards to each player and the dealer."""
    for _ in range(2):
        for player in players:
            card = player_states[player]['deck'].pop()
            player_states[player]['hand'].append(card)
        game_state['dealer_hand'].append(game_state['deck'].pop())


def calculate_score(hand):
    """Calculate the score of a hand."""
    score = 0
    aces = 0

    for card in hand:
        score += card_values[card]
        if card == 'A':
            aces += 1

    while aces > 0 and score > 21:
        score -= 10
        aces -= 1

    return score


def handle_player(player):
    """Handle a player's actions."""
    while True:
        try:
            action = player.recv(1024).decode()

            if action == 'hit':
                card = player_states[player]['deck'].pop()
                player_states[player]['hand'].append(card)
                player.send(str(player_states[player]['hand']).encode())

                if calculate_score(player_states[player]['hand']) > 21:
                    player.send("Bust!".encode())
            elif action == 'stand':
                player_states[player]['is_done'] = True
                player.send("Stand.".encode())
            elif action == 'double_down':
                if len(player_states[player]['hand']) == 2:
                    card = player_states[player]['deck'].pop()
                    player_states[player]['hand'].append(card)
                    player_states[player]['is_done'] = True
                    player.send(str(player_states[player]['hand']).encode())
                    if calculate_score(player_states[player]['hand']) > 21:
                        player.send("Bust!".encode())
                else:
                    player.send("Invalid move.".encode())
            elif action == 'quit':
                player.close()
                break
        except ConnectionResetError:
            player.close()
            break


# Wait for two players to connect
for _ in range(2):
    player, addr = server.accept()
    players.append(player)
    player_states[player] = {
        'hand': [],
        'deck': deck.copy(),
        'is_done': False
    }
    player.send(f'Welcome to the game! You are Player {len(players)}.'.encode())

# Deal initial cards
deal_initial_cards()

# Notify players of their initial hands
for player in players:
    player.send(str(player_states[player]['hand']).encode())

# Start player threads
threads = [threading.Thread(target=handle_player, args=(player,)) for player in players]
for thread in threads:
    thread.start()

# Handle the game logic
while True:
    current_player = players[game_state['player_turn']]
    other_player = players[(game_state['player_turn'] + 1) % 2]

    if player_states[current_player]['is_done']:
        game_state['player_turn'] = (game_state['player_turn'] + 1) % 2

    if player_states[current_player]['is_done'] and player_states[other_player]['is_done']:
        # Both players are done; dealer's turn
        while calculate_score(game_state['dealer_hand']) < 17:
            card = game_state['deck'].pop()
            game_state['dealer_hand'].append(card)

        dealer_score = calculate_score(game_state['dealer_hand'])
        for player in players:
            player.send(f"Dealer's hand: {game_state['dealer_hand']} (Score: {dealer_score})".encode())

        for player in players:
            player_score = calculate_score(player_states[player]['hand'])
            if player_score > 21:
                player.send("You bust! Dealer wins.".encode())
            elif dealer_score > 21:
                player.send("Dealer busts! You win.".encode())
            elif player_score == dealer_score:
                player.send("It's a tie! Push.".encode())
            elif player_score > dealer_score:
                player.send("You win!".encode())
            else:
                player.send("Dealer wins.".encode())

        # Reset game state for the next round
        for player in players:
            player_states[player]['hand'] = []
            player_states[player]['deck'] = deck.copy()
            player_states[player]['is_done'] = False
        game_state['deck'] = deck.copy()
        game_state['dealer_hand'] = []
        game_state['player_turn'] = 0

        # Deal initial cards for the next round
        deal_initial_cards()

        # Notify players of their initial hands for the next round
        for player in players:
            player.send(str(player_states[player]['hand']).encode())

# Close the server when done
server.close()