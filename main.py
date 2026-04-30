"""
Main module for the game.

The game controller instance is created here and is used to run the game.
"""

from controller import GameController


if __name__ == '__main__':
    game = GameController()
    game.gv.sl.load()
    game.run()
