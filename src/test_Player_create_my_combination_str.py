"""Module for testing create_my_combination_str from class Player."""
import unittest

from game import Player
from constants import COMBINATIONS, RANKS


class TestPlayerCreateMyCombinationStr(unittest.TestCase):
    """Class to test create_my_combination_str of class Player."""

    def setUp(self):
        """Set up for testing."""
        self.player1 = Player("A")
        comb1 = COMBINATIONS.index("Pair"), [RANKS.index("Q")], [RANKS.index("J"), RANKS.index("10"), RANKS.index("8")]
        self.player1.my_combination_tuple = comb1
        self.correct_my_combination_str1 = "Pair Q with another cards J 10 8"
        self.player2 = Player("B")
        comb2 = COMBINATIONS.index("Two Pairs"), [RANKS.index("A"), RANKS.index("J")], [RANKS.index("7")]
        self.player2.my_combination_tuple = comb2
        self.correct_my_combination_str2 = "Two Pairs A J with another cards 7"

    def test_str_pair(self):
        """Test string of pair."""
        self.player1.create_my_combination_str()
        self.assertEqual(self.player1.my_combination_str, self.correct_my_combination_str1)

    def test_str_two_pairs(self):
        """Test string of two pairs."""
        self.player2.create_my_combination_str()
        self.assertEqual(self.player2.my_combination_str, self.correct_my_combination_str2)


if __name__ == "__main__":
    unittest.main()
