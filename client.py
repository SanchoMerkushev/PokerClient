"""Client implementation."""
import socket
import json
import argparse
from time import sleep

from misc import recv_end, END


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
                output_string = "Your cards is {}".format(self.game_state["cards_on_hand"])
                print(output_string)
            if "balance" in self.game_state:
                output_string = "Your balance is {}".format(self.game_state["balance"])
                print(output_string)
            if "common_cards" in self.game_state:
                output_string = "Cards in table is {}".format(self.game_state["common_cards"])
                print(output_string)
            if "total_bids" in self.game_state:
                output_string = "Total bids in this round {}".format(self.game_state["total_bids"])
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
