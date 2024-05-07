"""Module for testing."""
import unittest

from combinations import count_combination
from constants import RANKS, SUITS, COMBINATIONS


def cards_to_numbers(cards):
    """Change name of cards to numbers for understandable testing."""
    result = []
    for card in cards:
        rank, suit = card.split("_")
        result.append((RANKS.index(rank), SUITS.index(suit)))
    return result


class TestCombinations(unittest.TestCase):
    """Class to test combinations.py."""

    def setUp(self):
        """Set up for testing."""
        self.cards1 = cards_to_numbers(("A_S", "K_S", "Q_S", "10_H", "8_D", "4_D", "2_D"))
        self.res1 = COMBINATIONS.index("High Card"), RANKS.index("A"), [RANKS.index("K"), RANKS.index("Q"),
                                                                        RANKS.index("10"), RANKS.index("8")]
        self.cards2 = cards_to_numbers(("A_S", "K_S", "A_S", "9_H", "10_D", "4_D", "K_D"))
        self.res2 = COMBINATIONS.index("Two Pairs"), [RANKS.index("A"), RANKS.index("K")], [RANKS.index("10")]
        self.cards3 = cards_to_numbers(("A_S", "K_S", "Q_S", "10_H", "8_D", "J_D", "2_D"))
        self.res3 = COMBINATIONS.index("Straight"), RANKS.index("A"), []
        self.cards4 = cards_to_numbers(("4_S", "3_S", "Q_S", "10_S", "8_S", "K_S", "2_D"))
        self.res4 = COMBINATIONS.index("Flush"), [RANKS.index("K"), RANKS.index("Q"),
                                                  RANKS.index("10"), RANKS.index("8"), RANKS.index("4")], []
        self.cards5 = cards_to_numbers(("8_S", "8_D", "A_S", "10_H", "10_D", "8_H", "10_S"))
        self.res5 = COMBINATIONS.index("Full House"), [RANKS.index("10"), RANKS.index("8")], []

    def test_high_cards(self):
        """Test combination High Card."""
        self.assertEqual(count_combination(self.cards1), self.res1)

    def test_two_pairs(self):
        """Test combination Two Pairs."""
        self.assertEqual(count_combination(self.cards2), self.res2)

    def test_straight(self):
        """Test combination Straight."""
        self.assertEqual(count_combination(self.cards3), self.res3)

    def test_flush(self):
        """Test combination Flush."""
        self.assertEqual(count_combination(self.cards4), self.res4)

    def test_full_house(self):
        """Test combination Full Housr."""
        self.assertEqual(count_combination(self.cards5), self.res5)


if __name__ == "__main__":
    unittest.main()
