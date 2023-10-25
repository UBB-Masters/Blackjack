import random


def initialize_deck():
    # Create a deck with 4 sets of 52 cards (standard deck)
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f'{rank} of {suit}' for rank in ranks for suit in suits] * 4
    random.shuffle(deck)
    return deck


def calculate_score(hand):
    score = 0
    aces = 0

    for card in hand:
        rank = card.split()[0]
        if rank == 'A':
            aces += 1
        else:
            score += 10 if rank in ['K', 'Q', 'J'] else int(rank)

    while aces > 0 and score + 11 <= 21:
        score += 11
        aces -= 1

    return score


class BlackjackGame:
    def __init__(self):
        self.deck = initialize_deck()
        self.player_hands = [[] for _ in range(2)]  # Two players
        self.current_player = 0  # Index of the player taking the current turn

    def start_game(self):
        # Deal two cards to each player
        for _ in range(2):
            for i in range(2):
                card = self.deck.pop()
                self.player_hands[i].append(card)

    def player_action(self, action):
        if action == 'hit':
            card = self.deck.pop()
            self.player_hands[self.current_player].append(card)
        elif action == 'stand':
            self.current_player = (self.current_player + 1) % 2

    def is_game_over(self):
        for hand in self.player_hands:
            if calculate_score(hand) > 21:
                return True
        return False

    def get_game_state(self):
        return {
            'player_hands': self.player_hands,
            'current_player': self.current_player,
            'is_game_over': self.is_game_over()
        }

    def determine_game_result(self):
        player_scores = [calculate_score(hand) for hand in self.player_hands]
        dealer_score = calculate_score(self.dealer_hand)

        results = []

        for score in player_scores:
            if score > 21:
                results.append("Bust")
            elif dealer_score > 21 or (score == 21 and len(self.player_hands[0]) == 2):
                results.append("Win")
            elif score > dealer_score:
                results.append("Win")
            elif score == dealer_score:
                results.append("Push")
            else:
                results.append("Lose")

        return results
