import sys
import curses
import time

import requests

from MagieModel import Menu
from Game import Game

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
        game.write_lines(['GOOD WORK!', 'YOU FINISHOS'] + game.level.levelName)

        time.sleep(MENU_PAUSE)

        game.write_lines(['Q .... QUITOS',
                          'C ... CHOOSOS',
                          'ANYTHING ELSE',
                          'TO PLAYOS'])

        choice = scr.getkey().upper()

        if choice == 'Q':
            quitos = True
        elif choice in ['M', 'B', 'U']:
            break


def guess_loop(scr: curses.window):
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    incorrect = curses.color_pair(1) | curses.A_BOLD
    correct = curses.color_pair(2) | curses.A_BOLD

    win_message = 'test'
    guess_message = ''
    i = 0
    guess_char = 'X'

    while guess_message != win_message:
        scr.refresh()
        if guess_char == win_message[i]:
            i += 1
            guess_message += guess_char

            scr.addstr(2, 2, guess_message, correct)
        else:
            scr.addstr(2, 2, guess_message, correct)
            scr.addstr(guess_char, incorrect)

        guess_char = chr(scr.getch())

    a = True

    for blinkquit in range(12):
        time.sleep(0.6)
        color = correct if a else incorrect
        a = not a
        scr.clear()
        scr.addstr(2, 2, 'CORRECT', color)
        scr.refresh()


if __name__ == '__main__':
    curses.wrapper(start_game, 'TestMenus/FullMenu.json')
