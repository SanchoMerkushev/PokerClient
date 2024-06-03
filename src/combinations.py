"""Game combinations."""
from src.constants import AMOUNT_RANKS, AMOUNT_SUITS


def count_combination(cards):
    """Count winning combination based on player hand."""
    ranks_count = [0] * AMOUNT_RANKS
    suits_list = [[] for _ in range(AMOUNT_SUITS)]
    for rank, suit in cards:
        ranks_count[rank] += 1
        suits_list[suit].append(rank)
    for i in range(AMOUNT_SUITS):
        suits_list[i].sort(reverse=True)
    ranks_count = ranks_count + ranks_count
    pair, second_pair, three_of_a_kind, straight, flush, four_of_a_kind = [None] * 6

    if all(ranks_count[AMOUNT_RANKS - 1: AMOUNT_RANKS] + ranks_count[:4]):
        straight = 3
    high_cards = []
    for i in range(AMOUNT_RANKS):
        if ranks_count[i] == 1:
            high_cards = [i] + high_cards
        if ranks_count[i] == 2:
            if pair is not None:
                second_pair = pair
            pair = i
        elif ranks_count[i] == 3:
            if three_of_a_kind is not None:
                pair = three_of_a_kind
            three_of_a_kind = i
        elif ranks_count[i] == 4:
            four_of_a_kind = i
        if i <= AMOUNT_RANKS - 5 and all(ranks_count[i:i+5]):
            straight = i + 5 - 1
    for i in range(AMOUNT_SUITS):
        if len(suits_list[i]) >= 5:
            flush = suits_list[i][:5]

    if straight is not None and flush is not None and straight == AMOUNT_RANKS - 1:
        return 9, [straight], []
    elif straight is not None and flush is not None:
        return 8, [straight], []
    elif four_of_a_kind is not None:
        return 7, [four_of_a_kind], high_cards[:1]
    elif pair is not None and three_of_a_kind is not None:
        return 6, [three_of_a_kind, pair], []
    elif flush is not None:
        return 5, flush, []
    elif straight is not None:
        return 4, [straight], []
    elif three_of_a_kind is not None:
        return 3, [three_of_a_kind], high_cards[:2]
    elif second_pair is not None:
        return 2, [pair, second_pair], high_cards[:1]
    elif pair is not None:
        return 1, [pair], high_cards[:3]
    else:
        return 0, [high_cards[0]], high_cards[1:5]
