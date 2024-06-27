"""Information print implementation."""
import gettext


translation = gettext.translation("msg", "po", fallback=True)
_ = translation.gettext


def cards_to_str(cards):
    """Print cards with Unicode."""
    res = []
    for rank, suit in cards:
        if rank == "X" and suit == "X":
            code = 0x1F0A0
        elif rank == "F" and suit == "F":
            code = 0x274C
        else:
            rank = (rank + 1) % 13
            code = 0x1F0A1 + rank + suit * 0x10
        res.append(chr(code))
    return "  ".join(res)


class UI():
    """Class for printing game information."""

    def print_state(self, state, my_name, my_cards):
        """Print all game info."""
        players_names = _("Players: \t")
        players_balances = _("Balances:\t")
        players_cards = _("Cards:   \t")
        players_bids = _("Bids:    \t")
        players_turns = _("Turns:   \t")
        for name in state["players"].keys():
            players_names += name + "\t"
            players_balances += str(state["players"][name]["balance"]) + "\t"
            players_bids += str(state["players"][name]["bid"]) + "\t"
            if name == my_name:
                players_cards += cards_to_str(my_cards) + "\t"
            else:
                players_cards += cards_to_str(state["players"][name]["cards"]) + "\t"
            if state["players"][name]["turn"]:
                players_turns += "*" + "\t"
            else:
                players_turns += " " + "\t"
        center = "\t"*((len(state["players"])*2 - 1)//2 - 1)
        bank = center + _("Bank: {}").format(state['sum_bids'])
        cards = center + cards_to_str(state["visible_cards"])
        ui = f"{players_names}\n{players_balances}\n{players_cards}\n{players_bids}\n{players_turns}\n\n{bank}\n{cards}"
        print(ui)
