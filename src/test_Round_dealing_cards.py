"""Module for testing dealing_cards from class Round."""
import unittest

from game import Round, Player
from constants import CARDS_ON_TABLE, CARDS_ON_HAND


class TestRoundDealingCards(unittest.TestCase):
    """Class to test dealing_cards of class Round."""

    def setUp(self):
        """Set up for testing."""
        self.players1 = [Player("A"), Player("B"), Player("C")]
        self.players2 = [Player(str(i)) for i in range(23)]

    def test_unique_cards(self):
        """Test that all cards is unique."""
        Testing_Round = Round(self.players1)
        Testing_Round.dealing_cards
        all_cards = set()
        for card in Testing_Round.table_cards:
            all_cards.add(card)
        for player in Testing_Round.players:
            for card in player.cards:
                all_cards.add(card)
        self.assertEqual(len(all_cards), CARDS_ON_TABLE + CARDS_ON_HAND * len(self.players1))

    def test_unique_cards2(self):
        """Test that all cards is unique."""
        Testing_Round = Round(self.players2)
        Testing_Round.dealing_cards
        all_cards = set()
        for card in Testing_Round.table_cards:
            all_cards.add(card)
        for player in Testing_Round.players:
            for card in player.cards:
                all_cards.add(card)
        self.assertEqual(len(all_cards), CARDS_ON_TABLE + CARDS_ON_HAND * len(self.players2))


if __name__ == "__main__":
    unittest.main()
