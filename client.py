"""Client implementation."""
import socket
import json
import argparse
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
        print(chr(code), end=" ")
    print()


class Client:
    """Client implementation."""

    def __init__(self, name, host, port):
        self.s = socket.create_connection((host, port))
        self.name = name
        self.s.sendall(f"{name}{END}".encode())

    def play(self):
        """Communicate with server, main loop for client."""
        while True:
            self.game_state = json.loads(recv_end(self.s, END))
            if "game_is_over" in self.game_state:
                self.s.close()
                break
            if "cards_on_hand" in self.game_state:
                output_string = "Your cards is: "
                print(output_string, end="")
                print_cards(self.game_state["cards_on_hand"])
            if "balance" in self.game_state:
                output_string = "Your balance is: {}$".format(self.game_state["balance"])
                print(output_string)
            if "common_cards" in self.game_state:
                output_string = "Cards on table is: "
                print(output_string, end="")
                print_cards(self.game_state["common_cards"])
            if "total_bids" in self.game_state:
                output_string = "Total bids in this round: {}$".format(self.game_state["total_bids"])
                print(output_string)
            if "output_inf" in self.game_state:
                output_string = self.game_state["output_inf"]
                print(output_string)
            sleep(0.1)
            if "answer" in self.game_state and self.game_state["answer"]:
                command = input() + END
                self.s.sendall(command.encode())


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    client = Client(args.name, 'localhost', 5000).play()
