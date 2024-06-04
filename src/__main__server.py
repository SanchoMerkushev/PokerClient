#!/usr/bin/env python3
"""Game server launcher."""
import socket

from src.game import Game, HumanPlayer
from src.misc import recv_end, END


if __name__ == "__main__":
    players = []
    s = socket.create_server(("", 5000))
    s.listen(4)
    for name in range(2):
        conn, addr = s.accept()
        name = recv_end(conn, END)
        players.append(HumanPlayer(name, conn, addr))
    s.close()

    Game(players, 2).start()
