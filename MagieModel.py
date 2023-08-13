import curses
import json
import time
from types import SimpleNamespace

TITLE_LINE =    '============='
SUBTITLE_LINE = '-------------'
LEVEL_START_PAUSE = 0.2

class Menu:
    def __init__(self, scr: curses.window, serialized='', file=None):
        self.categories = []
        if serialized:
            deserialized = json.loads(serialized, object_hook=lambda d: SimpleNamespace(**d))
        elif file:
            deserialized = json.load(file, object_hook=lambda d: SimpleNamespace(**d))
        else:
            return

        self.categories_by_name = deserialized.categories.__dict__

        for category_name, deserialized_category in self.categories_by_name.items():
            self.categories.append(Category(category_name, deserialized_category))

        self.category = None

        self.scr = scr


class Category:
    def __init__(self, name, deserialized):
        self.name = name
        self.sort_order = deserialized.sort_order
        self.levels = []

        for level in deserialized.levels:
            self.levels.append(Level(level))

        self.current_level = None


class Level:
    def __init__(self, deserialized = None):
        if not deserialized:
            deserialized = SimpleNamespace()

        self.levelName = deserialized.levelName or 'charlie is rad'
        self.puzzles = []
        self.current_puzzle_index = -1

        for puzzle in deserialized.puzzles:
            self.puzzles.append(Puzzle(puzzle))

    def go_to_next_puzzle(self):
        for index, puzzle in enumerate(self.puzzles):
            if not puzzle.isSolved:
                self.current_puzzle_index = index
                return

    def is_finished(self):
        for puzzle in self.puzzles:
            if not puzzle.isSolved:
                return False
        return True


class Puzzle:
    def __init__(self, deserialized):
        self.clue = deserialized.clue or []
        self.init = deserialized.init
        self.winText = deserialized.winText
        self.winMessage = deserialized.winMessage
        self.isSolved = False


class Game:
    def __init__(self, scr: curses.window, menu: Menu):
        self.scr = scr
        self.y = 0
        self.x = 0
        self.menu = menu
        self.category = None
        self.level = None
        self.puzzle = None

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.incorrect_color = curses.color_pair(1) | curses.A_BOLD
        self.correct_color = curses.color_pair(2) | curses.A_BOLD

    def reset(self):
        self.y = 0
        self.x = 0
        self.scr.clear()

    def write_lines(self, lines, indicator=''):
        if isinstance(lines, str):
            lines = lines.split('\n')

        if indicator:
            self.scr.addstr(self.y, self.x, indicator)
            self.x = len(indicator) + 1

        for line in lines:
            self.scr.addstr(self.y, self.x, line)
            self.y += 1

        self.x = 0

    def choose_category(self):
        self.reset()

        for index, category in enumerate(self.menu.categories):
            self.write_lines(category.name, f'{index}: ')

        self.y += 1

        self.write_lines('select category: ')
        category_number = int(chr(self.scr.getch()))
        self.category = self.menu.categories[category_number]

    def choose_level(self):
        self.reset()

        self.write_lines([self.category.name, TITLE_LINE])

        self.y += 1

        for index, level in enumerate(self.category.levels):
            self.write_lines(level.levelName, f'{index}: ')

        self.y += 1

        self.write_lines('select level: ')
        level_number = int(chr(self.scr.getch()))
        self.level = self.category.levels[level_number]

    def start_level(self):
        self.reset()

        if not self.level.puzzles:
            self.write_lines('No puzzles!')
            return

        if self.level.is_finished():
            self.reset()
            self.write_lines(self.level.levelName)
            self.y += 1
            self.write_lines('LEVEL FINISHED!')

        time.sleep(LEVEL_START_PAUSE)

        self.level.go_to_next_puzzle()

    def start_puzzle(self):
        self.reset()
        self.write_lines(self.level.levelName)
        self.write_lines(TITLE_LINE)

        self.y += 1

        puzzle = self.level.puzzles[self.level.current_puzzle_index]

        self.write_lines(puzzle.clue)
        self.write_lines(SUBTITLE_LINE)
        self.y += 1

        self.write_lines(puzzle.init)

        guess_char_index = len(puzzle.init)

        while not puzzle.isSolved:
            self.x = guess_char_index
            guess_char = chr(int(self.scr.getch(self.y, guess_char_index))).upper()
            if guess_char == puzzle.winText[guess_char_index]:
                self.scr.addch(self.y, guess_char_index, guess_char, self.correct_color)
                guess_char_index += 1
                puzzle.isSolved = guess_char_index >= len(puzzle.winText)
            else:
                self.scr.addch(self.y, guess_char_index, guess_char, self.incorrect_color)

        self.x = 0
        self.y += 1
        self.write_lines(puzzle.winMessage)
        self.scr.getch(self.y, self.x)