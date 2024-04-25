from constants import *

def count_combination(cards):
    ranks_count = [0] * AMOUNT_RANKS
    suits_count = [0] * AMOUNT_SUITS
    for rank, suit in cards:
        ranks_count[rank] += 1
        suits_count[suit] += 1
    ranks_count = ranks_count + ranks_count
    pair, second_pair, three_of_a_kind, straight, flush, four_of_a_kind = [None] * 6
    if all(ranks_count[AMOUNT_RANKS - 1: AMOUNT_RANKS] + ranks_count[:4]):
        straight = -1 + 5 - 1
    high_cards = []
    for i in range(AMOUNT_RANKS):
        if ranks_count[i] == 1:
            high_cards = [i] + high_cards
        if ranks_count[i] == 2:
            if pair:
                second_pair = pair
            pair = i
        elif ranks_count[i] == 3:
            three_of_a_kind = i
        elif ranks_count[i] == 4:
            four_of_a_kind = i
        if i <= AMOUNT_RANKS - 5 and all(ranks_count[i:i+5]):
            straight = i + 5 - 1
    for i in range(AMOUNT_SUITS):
        if suits_count[i] >= 5:
            for j in range(AMOUNT_RANKS):
                if ranks_count[j]:
                    flush = j
    if straight is not None and flush is not None and straight == AMOUNT_RANKS - 1:
        return "Royal Flush", None, None
    elif straight is not None and flush is not None:
        return "Straight Flush", straight, None
    elif four_of_a_kind is not None:
        return "Four of a Kind", four_of_a_kind, high_cards[:1]
    elif pair is not None and three_of_a_kind is not None:
        return "Full House", (three_of_a_kind, pair), None
    elif flush is not None:
        return "Flush", flush, None
    elif straight is not None:
        return "Straight", straight, None
    elif three_of_a_kind is not None:
        return "Three of a Kind", three_of_a_kind, high_cards[:2]
    elif second_pair is not None:
        return "Two Pairs", (pair, second_pair), high_cards[:1]
    elif pair is not None:
        return "Pair", pair, high_cards[:3]
    else:
        return "High Card", None, high_cards[:5]


test_cards = ((1, 2), (5, 2), (4, 2), (7, 2), (8, 2), (6, 1), (11, 2))
print(count_combination(test_cards))
test_cards = ((0, 1), (0, 2), (8, 1), (8, 2), (7, 3), (4, 1), (4, 2))
print(count_combination(test_cards))
test_cards = ((0, 1), (0, 2), (8, 1), (8, 2), (0, 3), (4, 1), (4, 2))
print(count_combination(test_cards))
test_cards = ((0, 1), (1, 2), (8, 1), (8, 2), (9, 3), (4, 1), (5, 2))
print(count_combination(test_cards))
test_cards = ((0, 1), (1, 1), (4, 1), (8, 1), (9, 1), (6, 1), (5, 2))
print(count_combination(test_cards))
