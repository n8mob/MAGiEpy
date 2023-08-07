import sys
import curses
import time

import requests

from MagieModel import Game, Menu


def start_game(scr: curses.window, json_path):
    with open(json_path) as menu_file:
        full_menu = Menu(scr, file=menu_file)

    game = Game(scr, full_menu)

    game.choose_level()

    game.start_level()

    scr.getch()


def choose_from_dict(choices, prompt):
    choice_menu = list(choices.keys())
    for i, choice_name in enumerate(choice_menu):
        print(f"{i}: {choice_name}")
    choice = input(prompt + ' ')
    if str.isnumeric(choice):
        return choices[choice_menu[int(choice)]]
    else:
        return choices[choice]


def choose_from_list(choices, prompt):
    for i, choice_name in enumerate(choices):
        print(f'\n{i}: {choice_name}')

    choice = input(prompt + ' ')
    return int(choice)


def try_a_puzzle(scr: curses.window):
    url = 'https://puzzles.magiegame.com/menus/'
    response = requests.get(url)
    category_menu = CategoryMenu(response.json()[0])
    chosen_category = choose_from_dict(category_menu.categories_by_name, 'which category?')
    for level in chosen_category:
        for puzzle in level['puzzles']:
            print()
            CategoryMenu.print(puzzle['clue'])
            print()
            CategoryMenu.print(puzzle['init'])

            guess_phrase = None
            guess_char = None
            win_index = 0
            win_char = puzzle['winText'][win_index]

            while guess_phrase != puzzle['winText']:
                guess_char = scr.getch()
                if guess_char == win_char:
                    print(puzzle['winText'][:win_index])
                else:
                    print('\b')

            print('\nCORRECT')


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
