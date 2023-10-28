from BlackJack.Player import Player

cards = ["2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A"]
colors = ["Heart", "Spades", "Diamond", "Trefle"]


class Blackjack:
    def __init__(self, _player1: Player, _player2: Player, _deck):
        self.player1 = _player1
        self.player2 = _player2
        self.deck = _deck

    def startGame(self):
        pass
