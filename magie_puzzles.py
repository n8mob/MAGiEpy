import sys
import curses
import time

import requests

from MagieModel import Menu
from Game import Game, SUBTITLE_LINE, TITLE_LINE
from magie_display import MAGiEDisplay, ColorScheme


def start_game(scr: curses.window, json_path):
    with open(json_path) as menu_file:
        menu = Menu(scr, file=menu_file)

    magie = MAGiEDisplay(scr, ColorScheme.default_color_scheme())

    game = Game(menu, magie)
    game.run()


if __name__ == '__main__':
    curses.wrapper(start_game, 'TestMenus/FullMenu.json')
