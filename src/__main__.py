#!/usr/bin/env python3
"""Game client launcher."""
import argparse
import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from src.client import Client


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="name", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    client = Client(args.name, 'localhost', 5000).cmdloop()
