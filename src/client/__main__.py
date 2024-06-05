#!/usr/bin/env python3
"""Game client launcher."""
import argparse

from .client import Client


def client_main():
    """Receive information about player and create Client."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()
    Client(args.name, 'localhost', 5000).cmdloop()


if __name__ == "__main__":
    client_main()
