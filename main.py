#!/usr/bin/env python3
"""Deep Jungle — entry point.

Run this file to start the game:
    python main.py
"""
from game.app import Game


def main() -> None:
    """Create a Game instance and run it."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
