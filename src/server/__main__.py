#!/usr/bin/env python3
"""Game server launcher."""
import socket
import argparse
import gettext

from .game import Game, HumanPlayer, ComputerPlayer, SelfPlayer
from .misc import recv_end, END


translation = gettext.translation("msg", "po", fallback=True)
_ = translation.gettext


def server_main():
    """Server recieve players."""
    players = []
    s = socket.create_server(("", 5000))
    s.listen(4)
    for name in range(2):
        conn, addr = s.accept()
        name = recv_end(conn, END)
        players.append(HumanPlayer(name, conn, addr))
    s.close()

    Game(players, 2).start()


def local_main():
    """Local play with bots."""
    players = []
    print(_("Enter your name:"))
    self_name = input()
    players.append(SelfPlayer(self_name))
    print(_("Enter amount of bots:"))
    amount_players = int(input())
    while amount_players <= 0 or amount_players > 5:
        print(_("Amount of bots must be between 1 and 5!"))
        amount_players = int(input())
    names = ["Alice", "Bob", "Chris", "Denis", "Eva"]
    print(_("Choose aggression of player between -5 and 5"))
    for i in range(amount_players):
        print(_("Aggression for {}:").format(names[i]))
        players.append(ComputerPlayer(names[i], int(input())))
    Game(players, 10).start()


if __name__ == "__main__":
    local_main()
