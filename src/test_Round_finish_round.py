"""Module for testing finish_round from class Round."""
import unittest

from game import Round, Player
from constants import RANKS


class TestFinishRound(unittest.TestCase):
    """Class to test finish_round of class Round."""

    def setUp(self):
        """Set up for testing."""
        self.players = [Player("A"), Player("B"), Player("C")]
        self.test_round = Round(self.players)
        for player in self.players:
            player.balance = 700
        self.players[0].cards = [(RANKS.index("A"), 1), (RANKS.index("A"), 2)]
        self.players[1].cards = [(RANKS.index("K"), 1), (RANKS.index("K"), 2)]
        self.players[2].cards = [(RANKS.index("10"), 1), (RANKS.index("9"), 2)]
        cur_cards = [(RANKS.index("A"), 0), (RANKS.index("K"), 0),
                     (RANKS.index("10"), 3), (RANKS.index("9"), 3), (RANKS.index("K"), 3)]
        self.test_round.table_cards = cur_cards
        self.test_round.sum_bids = 900

    def test_change_balance_after_winning(self):
        """Test changing of balance."""
        self.test_round.finish_round()
        balances = tuple(int(player.balance) for player in self.players)
        self.assertEqual(balances, (700, 1600, 700))


if __name__ == "__main__":
    unittest.main()
