"""Client implementation."""
import socket
import json
import argparse
import cmd
import os
import gettext
from time import sleep

from misc import recv_end, END


translation = gettext.translation("msg", "po", fallback=True)
_ = translation.gettext


def cards_to_str(cards):
    """Print cards with Unicode."""
    res = []
    for rank, suit in cards:
        if rank == "X" and suit == "X":
            code = 0x1F0A0
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
        os.system("clear")
        ui = f"{players_names}\n{players_balances}\n{players_cards}\n{players_bids}\n{players_turns}\n\n{bank}\n{cards}"
        print(ui)


class Client(cmd.Cmd):
    """Client implementation."""

    def __init__(self, name, host, port):
        super().__init__()
        self.s = socket.create_connection((host, port))
        self.name = name
        self.prompt = f"{name}>"
        self.s.sendall(f"{name}{END}".encode())
        self.my_turn = False
        self.ui = UI()
        self.cards = None
        self.play()

    def play(self):
        """Communicate with server, main loop for client."""
        while True:
            self.game_state = json.loads(recv_end(self.s, END))
            if "sync" in self.game_state:
                self.ui.print_state(self.game_state, self.name, self.cards)
            if "game_is_over" in self.game_state:
                self.s.close()
                exit()
            if "cards_on_hand" in self.game_state:
                self.cards = self.game_state["cards_on_hand"]
            if "output_inf" in self.game_state:
                output_string = self.game_state["output_inf"]
                print(output_string)
                sleep(0.2)
            if "finish_round" in self.game_state:
                output_string = self.game_state["finish_round"]
                print(output_string)
            if "answer" in self.game_state and self.game_state["answer"]:
                self.my_turn = True
                break

    def do_RAISE(self, arg):
        """Raise bid."""
        if not self.my_turn:
            print(_("It's not your turn."))
        try:
            arg = int(arg)
            if arg < 1:
                raise ValueError
        except ValueError:
            print(_("RAISE value must be integer bigger than one."))
            return
        command = f"RAISE {arg}{END}"
        self.s.sendall(command.encode())
        self.my_turn = False
        self.play()

    def do_CALL(self, arg):
        """Call bid."""
        if not self.my_turn:
            print(_("It's not your turn."))
        if arg != "":
            print(arg)
            print(_("CALL doesn't need any arguments."))
            return
        command = f"CALL{END}"
        self.s.sendall(command.encode())
        self.my_turn = False
        self.play()

    def do_FOLD(self, arg):
        """Fold cards."""
        if not self.my_turn:
            print(_("It's not your turn."))
        if arg != "":
            print(_("FOLD doesn't need any arguments."))
            return
        command = f"FOLD{END}"
        self.s.sendall(command.encode())
        self.my_turn = False
        self.play()

    def default(self, arg):
        """Print error."""
        print(_("Unknown command:"), arg)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    client = Client(args.name, 'localhost', 5000).cmdloop()
