from random import shuffle

card_colors = ["Diamonds", "Hearts", "Spades", "Clubs"]
card_values = {
    'A': 11,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}


class Card:
    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.value = card_values[number]

    def __str__(self):
        return f"{self.number} of {self.color}"


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def get_score(self):
        total = sum(card.value for card in self.hand)
        aces = [card for card in self.hand if card.number == 'A']
        while total > 21 and aces:
            aces.pop()
            total -= 10  # Convert 'A' from 11 to 1 if the total exceeds 21.
        return total

    def __str__(self):
        return f"{self.name}'s Hand: [{', '.join(map(str, self.hand))}]"


class Dealer:
    def __init__(self):
        self.hand = []

    def get_score(self):
        total = sum(card.value for card in self.hand)
        aces = [card for card in self.hand if card.number == 'A']
        while total > 21 and aces:
            aces.pop()
            total -= 10  # Convert 'A' from 11 to 1 if the total exceeds 21.
        return total

    def __str__(self):
        return f"Dealer's Hand: [{', '.join(map(str, self.hand))}]"


class Deck:
    def __init__(self):
        self.cards = [Card(number, color) for color in card_colors for number in card_values.keys()]
        shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Blackjack:
    def __init__(self):
        self.players = [Player(input("Player 1, say your name: ")), Player(input("Player 2, say your name: "))]
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.players = self.players

    def play_game(self):
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.deal_card())
            self.dealer.hand.append(self.deck.deal_card())

        for player in self.players:
            print(player, player.get_score())
        print(self.dealer, self.dealer.get_score())

        for player in self.players:
            self.take_turn(player)
            print(player)

        self.dealer_turn()
        print(self.dealer)

        for player in self.players:
            if player.get_score() > 21:
                print(f"{player.name} busted!")

        dealer_score = self.dealer.get_score()
        winning_players = [player for player in self.players if
                           player.get_score() <= 21 and player.get_score() > dealer_score]

        if dealer_score <= 21 and not winning_players:
            print("Dealer is the overall winner!")
        elif winning_players:
            print("The following players win:")
            for player in winning_players:
                print(player.name)

    def take_turn(self, player):
        while True:
            action = input(f"{player.name}, do you want to (h)it or (s)tand? ").lower()
            if action == 'h':
                player.hand.append(self.deck.deal_card())
                print(player, player.get_score())
                if player.get_score() > 21:
                    print(f"{player.name} busted!")
                    break
            elif action == 's':
                break
            else:
                print("Invalid action, try again")

    def dealer_turn(self):
        while self.dealer.get_score() < 17:
            self.dealer.hand.append(self.deck.deal_card())


if __name__ == "__main__":
    game = Blackjack()
    game.play_game()
