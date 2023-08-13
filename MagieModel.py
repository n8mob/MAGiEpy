import curses
import json
from types import SimpleNamespace

TITLE_LINE =    '============='
SUBTITLE_LINE = '-------------'


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

        for puzzle in deserialized.puzzles:
            self.puzzles.append(Puzzle(puzzle))


class Puzzle:
    def __init__(self, deserialized):
        self.clue = deserialized.clue or []
        self.init = deserialized.init


class Line:
    pass


class Game:
    def __init__(self, scr: curses.window, menu: Menu):
        self.scr = scr
        self.y = 0
        self.x = 0
        self.menu = menu
        self.category = None
        self.level = None
        self.puzzle = None

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

        self.write_lines(self.level.levelName)
        self.write_lines(TITLE_LINE)

        if not self.level.puzzles:
            self.write_lines('No puzzles!')
            return

        self.puzzle = self.level.puzzles[0]

        self.y += 1

        self.write_lines(self.puzzle.clue)
        self.write_lines(SUBTITLE_LINE)

        self.y += 1

        self.write_lines(self.puzzle.init)

