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
        self.type = deserialized.type
        self.encoding = deserialized.encoding

