import sys
import curses
import time

import requests

from MagieModel import Menu
from Game import Game, SUBTITLE_LINE, TITLE_LINE

MENU_PAUSE = 0.4


def start_game(scr: curses.window, json_path):
    with open(json_path) as menu_file:
        full_menu = Menu(scr, file=menu_file)

    game = Game(scr, full_menu)

    quitos = False

    game.choose_category()

    while not quitos:
        game.choose_level()

        game.start_level()

        while not game.level.is_finished():
            game.start_puzzle()

            game.level.go_to_next_puzzle()

        game.write_text([SUBTITLE_LINE, '', 'GOOD WORK!', 'YOU FINISHOS'] + game.level.levelName)

        time.sleep(MENU_PAUSE)
        game.write_text(TITLE_LINE)

        game.write_text(['Q .... QUITOS',
                          'C ... CHOOSOS',
                          'ANYTHING ELSE',
                          'TO PLAYOS'])

        choice = scr.getkey().upper()

        if choice == 'Q':
            quitos = True
        elif choice in ['M', 'B', 'U']:
            break


if __name__ == '__main__':
    curses.wrapper(start_game, 'TestMenus/MinimalMenu.json')
