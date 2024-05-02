"""Client implementation."""
import socket
import json
import argparse

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
            print(self.game_state)
            if "game_is_over" in self.game_state:
                self.s.close()
                break
            if self.game_state["players"][self.name]["turn"]:
                command = input() + END
                self.s.sendall(command.encode())


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    client = Client(args.name, 'localhost', 5000).play()
