"""Client implementation."""
import socket
import json

from misc import recv_end


class Client:
    """Client implementation."""

    def __init__(self, host, port):
        self.s = socket.create_connection((host, port))
        self.END = "@@@END@@@"

    def play(self):
        """Communicate with server, main loop for client."""
        while True:
            self.game_state = json.loads(recv_end(self.s, self.END))
            print(self.game_state)


client = Client('localhost', 5000).play()
