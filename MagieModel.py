import curses
import json
from types import SimpleNamespace



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
        self.levels = deserialized.levels
        self.current_level = None

    def prompt_for_level(self, scr):
        output_line = 0

        for i, level in enumerate(self.levels):
            choice_indicator = f'{i}: '
            scr.addstr(output_line, 0, choice_indicator)
            left_margin = len(choice_indicator)
            for line in level.name_lines:
                scr.addstr(output_line, left_margin, f'{line}')
                output_line += 1

        level_number = int(chr(scr.getch()))
        self.current_level = self.levels[level_number]
        return  self.current_level


class Level:
    def __init__(self, deserialized):
        self.levelName = deserialized.levelName or []
        self.puzzles = deserialized.puzzles or []


class Puzzle:
    def __init__(self, deserialized):
        self.clue = deserialized.clue or []


class Line:
    pass


class Game:
    def __init__(self, scr: curses.window, menu: Menu):
        self.scr = scr
        self.menu = menu
        self.category = None
        self.level = None
        self.puzzle = None

    def write_lines(self, lines, indicator='', y=0, x=0):
        self.scr.addstr(y, x, indicator)
        x += len(indicator) + 1

        for line in lines:
            self.scr.addstr(y, x, line)
            y += 1

        return y

    def choose_category(self):
        y = 0

        self.scr.clear()

        for category in self.menu.categories:
            self.write_lines([category.name], f'{y}: ', y, 0)
            y += 1

        y += 1

        self.scr.addstr(y, 0, 'select category: ')
        category_number = int(chr(self.scr.getch()))
        self.category = self.menu.categories[category_number]

    def choose_level(self):
        self.scr.clear()

        self.write_lines(self.category.name)

        y = 2

        for index, level in enumerate(self.category.levels):
            y = self.write_lines(level.levelName, f'{index}: ', y, 0)

        y += 1

        self.scr.addstr(y, 0, 'select level: ')
        level_number = int(chr(self.scr.getch()))
        self.level = self.category.levels[level_number]
        self.puzzle = self.level[0]

    def start_level(self):
        self.scr.clear()
        self.write_lines(self.level.levelName)

        y = len(self.level.levelName) + 2

        y = self.write_lines(self.puzzle.clue)

        y += 1

        y = self.write_lines(self.puzzle.init)

