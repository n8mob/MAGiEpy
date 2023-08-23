import curses
import json

from Encodings import FixedWidthEncoding, BinaryEncoding

DEFAULT_ENCODING = '5bA1'

DEFAULT_PUZZLE_TYPE = 'Decode'


class Menu:
    def __init__(self, scr: curses.window, serialized='', file=None):
        if serialized:
            deserialized = json.loads(serialized)
        elif file:
            deserialized = json.load(file)
        else:
            return

        self.encodings = {}
        for encoding_id, encoding in deserialized['encodings'].items():
            if encoding['type'] == 'fixed':
                self.encodings[encoding_id] = FixedWidthEncoding(encoding['width'], encoding['encoding'])
            else:
                self.encodings[encoding_id] = BinaryEncoding(encoding)

        self.categories_by_name = {}
        self.categories = []

        for category_name, deserialized_category in deserialized['categories'].items():
            category = Category(category_name, deserialized_category, self)
            self.categories_by_name[category_name] = category
            self.categories.append(category)

        self.category = None

        self.scr = scr


class Category:
    next_sort = 0

    def __init__(self, name, deserialized, menu):
        self.name = name
        self.menu = menu
        self.sort_order = deserialized.get('sort_order', Category.next_sort)
        Category.next_sort = self.sort_order + 1
        self.levels = []

        for level in deserialized['levels']:
            self.levels.append(Level(level, menu))

        self.current_level = None


class Puzzle:
    def __init__(self, deserialized=None, menu=None):
        if not deserialized:
            deserialized = {}

        self.menu = menu
        self.puzzleName = deserialized.get('puzzleName', '')

        self.clue = deserialized.get('clue', None)
        if not self.clue:
            self.clue = []

        self.init = deserialized.get('init', '')
        if not self.init:
            self.init = ''

        self.winText = deserialized.get('winText', '')
        if not self.winText:
            self.winText = ''
        self.winMessage = deserialized.get('winMessage', [])
        self.isSolved = False
        self.type = deserialized.get('type', DEFAULT_PUZZLE_TYPE)
        self.encoding_id = deserialized.get('encoding', DEFAULT_ENCODING)
        if not menu or not menu.encodings or self.encoding_id not in menu.encodings:
            raise ValueError(f'Cannot find encoding {self.encoding_id} in menu.encodings')

        self.encoding = menu.encodings[self.encoding_id]


class Level:
    def __init__(self, deserialized=None, menu=None):
        if not deserialized:
            deserialized = {}

        self.menu = menu
        self.levelName = deserialized.get('levelName', [])
        self.puzzles: [Puzzle] = []
        self.current_puzzle_index = -1

        for puzzle in deserialized.get('puzzles', []):
            self.puzzles.append(Puzzle(puzzle, menu))

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

    def get_current_puzzle(self) -> Puzzle:
        """The puzzle currently being played for this level"""
        return self.puzzles[self.current_puzzle_index]
