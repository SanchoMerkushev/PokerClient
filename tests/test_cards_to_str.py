"""Module for testing cards_to_str."""
import unittest

from src.client import cards_to_str
from src.constants import RANKS, SUITS


class TestCardsToUnicode(unittest.TestCase):
    """Class to test cards to Unicode image."""

    def setUp(self):
        """Set up for testing."""
        self.cards = ((RANKS.index("A"), SUITS.index("S")), (RANKS.index("8"), SUITS.index("D")))
        self.unicode_symbols = chr(0x1F0A1) + "  " + chr(0x1F0C8)

    def test_cards_to_unicode(self):
        """Test cards to Unicode."""
        self.assertEqual(cards_to_str(self.cards), self.unicode_symbols)


if __name__ == "__main__":
    unittest.main()
