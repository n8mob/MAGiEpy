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

        for category_name, category in self.categories_by_name.items():
            category.name = category_name
            self.categories.append(category)

        self.scr = scr

    def print_menu_choice(self):
        output_line = 0

        for category in self.categories:
            self.scr.addstr(output_line, 0, f'{output_line}: {category.name}')
            output_line += 1

        self.scr.addstr(output_line, 0, '\n\nSelect category: ')
        category_number = int(chr(self.scr.getch()))

        output_line += 3

        self.scr.addstr(output_line, 0, f'selected {category_number}: {self.categories[category_number].name}')

        # TODO hand off to category to print list of levels


class Category:
    def __init__(self, levels=None):
        self.levels = levels or []


class Level:
    def __init__(self, name_lines=None, puzzles=None):
        self.name_lines = name_lines or []
        self.puzzles = puzzles or []


class Puzzle:
    def __init__(self, clue_lines=None, win_text=None, init_text=None):
        self.clue_lines = clue_lines or []
        self.win_text = win_text or ''
        self.init_text = init_text or ''


class Line:
    pass
