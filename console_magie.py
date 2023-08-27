import sys
import time

import requests

from MagieModel import Menu
from Game import Game, SUBTITLE_LINE, TITLE_LINE
from magie_display import ColorScheme, ConsoleMAGiE


def start_game(json_path):
    with open(json_path) as menu_file:
        menu = Menu(file=menu_file)

    magie = ConsoleMAGiE()

    game = Game(menu, magie)
    game.run()


if __name__ == '__main__':
    start_game('TestMenus/FullMenu.json')
