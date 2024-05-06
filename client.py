"""Client implementation."""
import socket
import json
import argparse
import cmd
from time import sleep

from misc import recv_end, END


def print_cards(cards):
    """Print cards with Unicode."""
    for rank, suit in cards:
        if rank == "X" and suit == "X":
            code = 0x1F0A0
        else:
            rank = (rank + 1) % 13
            code = 0x1F0A1 + rank + suit * 0x10
        print(chr(code), end="  ")
    print()


class Client(cmd.Cmd):
    """Client implementation."""

    def __init__(self, name, host, port):
        super().__init__()
        self.s = socket.create_connection((host, port))
        self.name = name
        self.s.sendall(f"{name}{END}".encode())
        self.my_turn = False
        self.play()

    def play(self):
        """Communicate with server, main loop for client."""
        while True:
            self.game_state = json.loads(recv_end(self.s, END))
            if "game_is_over" in self.game_state:
                self.s.close()
                exit()
            if "cards_on_hand" in self.game_state:
                output_string = "Your cards is"
                print(output_string)
                print_cards(self.game_state["cards_on_hand"])
            if "balance" in self.game_state:
                output_string = "Your balance is {}".format(self.game_state["balance"])
                print(output_string)
            if "common_cards" in self.game_state:
                output_string = "Cards on table is"
                print(output_string)
                print_cards(self.game_state["common_cards"])
            if "total_bids" in self.game_state:
                output_string = "Total bids in this round {}".format(self.game_state["total_bids"])
                print(output_string)
            if "output_inf" in self.game_state:
                output_string = self.game_state["output_inf"]
                print(output_string)
            sleep(0.1)
            if "answer" in self.game_state and self.game_state["answer"]:
                self.my_turn = True
                break

    def do_raise(self, arg):
        """Raise bet."""
        if not self.my_turn:
            print("It's not your turn.")
        try:
            arg = int(arg)
            if arg < 1:
                raise ValueError
        except ValueError:
            print("RAISE value must be integer bigger than one.")
            return
        command = f"RAISE {arg}{END}"
        self.s.sendall(command.encode())
        self.play()

    def do_call(self, arg):
        """Call bet."""
        if not self.my_turn:
            print("It's not your turn.")
        if arg != "":
            print(arg)
            print("CALL doesn't need any arguments.")
            return
        command = f"CALL{END}"
        self.s.sendall(command.encode())
        self.play()

    def do_fold(self, arg):
        """Fold cards."""
        if not self.my_turn:
            print("It's not your turn.")
        if arg != "":
            print("FOLD doesn't need any arguments.")
            return
        command = f"FOLD{END}"
        self.s.sendall(command.encode())
        self.play()


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    client = Client(args.name, 'localhost', 5000).cmdloop()
