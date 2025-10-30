import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project.game_bot import Bot
from project.game_play import Game


def main():
    bots = [
        Bot("Bot 1", 1000),
        Bot("Bot 2", 800),
        Bot("Bot 3", 600),
        Bot("Bot 4", 400),
        Bot("Bot 5", 200),
        Bot("Bot 6", 50),
    ]
    game = Game(bots, max_rounds=10)
    game.play()


if __name__ == "__main__":
    main()
