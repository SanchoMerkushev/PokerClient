"""Bot logic."""
from .constants import BIG_BLIND_SIZE, ALL_CARDS
from random import randrange
from itertools import combinations
from .combinations import count_combination


def is_small(n):
    """Count is bid small or not."""
    return n <= 3 * BIG_BLIND_SIZE


def is_middle(n):
    """Count is bid middle or not."""
    return 3 * BIG_BLIND_SIZE < n <= 6 * BIG_BLIND_SIZE


def is_big(n):
    """Count is bid big or not."""
    return 6 * BIG_BLIND_SIZE < n


def power_hand_preflop(my_cards):
    """Count power of hand in preflop."""
    rank1, suit1 = my_cards[0]
    rank2, suit2 = my_cards[1]
    power_hand = 0
    if rank1 == rank2:
        power_hand += 5
    if max(rank1, rank2) > 4:
        power_hand += 2
    elif max(rank1, rank2) > 6:
        power_hand += 3
    elif max(rank1, rank2) > 8:
        power_hand += 4
    elif max(rank1, rank2) > 10:
        power_hand += 5
    if rank1 != rank2 and min(rank1, rank2) > 8:
        power_hand += 2
    elif rank1 != rank2 and min(rank1, rank2) > 10:
        power_hand += 3
    if suit1 == suit2:
        power_hand += 2
    return power_hand


def power_hand_flop(my_cards, visible_cards):
    """Count power of hand after preflop."""
    cards = set(ALL_CARDS)
    for card in visible_cards:
        cards.remove(card)
    all_combinations = []
    for cur_hand in combinations(cards, 2):
        all_combinations.append(count_combination(visible_cards + list(cur_hand)))
    all_combinations.sort()
    amount = len(all_combinations)
    my_pos = all_combinations.index(count_combination(visible_cards + list(my_cards)))
    power_hand = int(my_pos / amount * 10)
    return power_hand


def decision(my_cards, visible_cards, bid, max_raise, my_balance, aggresive=0):
    """Make decision to CALL or FOLD por RAISE."""
    amount_visible = 0
    while amount_visible < len(visible_cards) and visible_cards[amount_visible] != "XX":
        amount_visible += 1
    if amount_visible == 0:
        power_hand = power_hand_preflop(my_cards)
    else:
        power_hand = power_hand_flop(my_cards, visible_cards[:amount_visible])
    if power_hand < 9 or power_hand > 1:
        power_hand += aggresive
    power_hand = min(power_hand, 10)
    power_hand = max(power_hand, 0)
    if randrange(15) <= aggresive and not is_big(bid):
        power_hand = 10
    if is_big(bid) and power_hand < 7 or is_middle(bid) and power_hand < 5 or is_small(bid) and power_hand < 2:
        return ("FOLD", 0)
    if is_big(bid) and power_hand < 10 or is_middle(bid) and power_hand < 7 or is_small(bid) and power_hand < 5:
        return ("CALL", 0)
    max_bid = min(max_raise, my_balance)
    if power_hand >= 9 and max_bid >= BIG_BLIND_SIZE:
        return ("RAISE", randrange(BIG_BLIND_SIZE, max_bid + 1, BIG_BLIND_SIZE))
    if power_hand >= 7 and max_bid >= BIG_BLIND_SIZE:
        return ("RAISE", randrange(BIG_BLIND_SIZE, (max_bid + 1) // 2, BIG_BLIND_SIZE))
    return ("CALL", 0)
