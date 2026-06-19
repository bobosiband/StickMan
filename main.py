#!/usr/bin/env python3

from game.app import Game


def main() -> None:
    """Create a Game instance and run it."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
