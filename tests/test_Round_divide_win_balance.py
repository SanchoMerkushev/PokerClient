"""Module for testing finish_round from class Round with two winners."""
import unittest

from src.server.game import Round, Player
from src.server.constants import RANKS


class TestFinishRound(unittest.TestCase):
    """Class to test finish_round of class Round."""

    def setUp(self):
        """Set up for testing."""
        self.players = [Player("A"), Player("B"), Player("C")]
        self.test_round = Round(self.players)
        for player in self.players:
            player.balance = 600
        self.players[0].cards = [(RANKS.index("A"), 1), (RANKS.index("A"), 2)]
        self.players[1].cards = [(RANKS.index("J"), 3), (RANKS.index("J"), 2)]
        self.players[2].cards = [(RANKS.index("A"), 3), (RANKS.index("A"), 0)]
        cur_cards = [(RANKS.index("Q"), 0), (RANKS.index("K"), 0),
                     (RANKS.index("10"), 3), (RANKS.index("4"), 3), (RANKS.index("K"), 3)]
        self.test_round.table_cards = cur_cards
        self.test_round.sum_bids = 1200

    def test_change_balance_after_winning_two_winners(self):
        """Test changing of balance, two winners."""
        self.test_round.finish_round()
        balances = tuple(int(player.balance) for player in self.players)
        self.assertEqual(balances, (1200, 600, 1200))


if __name__ == "__main__":
    unittest.main()
