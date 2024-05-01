import json
import logging
from enum import Enum
from typing import Any

from binary_encoding import BinaryEncoding
from fixed_width import FixedWidthEncoding
from variable_width import VariableWidthEncoding
from xor_encoding import XorEncoding

DEFAULT_ENCODING = '5bA1'
DEFAULT_ENCODING_WIDTH = 5
DEFAULT_PUZZLE_TYPE = 'Decode'


class Menu:
  encodings: dict[Any, BinaryEncoding]

  def __init__(self, deserialized=None, serialized='', file=None):
    self.log = logging.getLogger(__name__)
    if not deserialized:
      if serialized:
        deserialized = json.loads(serialized)
      elif file:
        deserialized = json.load(file)
      else:
        deserialized = {}

    self.encodings = {}
    if 'encodings' in deserialized:
      for encoding_id, encoding in deserialized['encodings'].items():
        if encoding['type'] == 'fixed':
          width = encoding['width'] if 'width' in encoding else DEFAULT_ENCODING_WIDTH
          self.encodings[encoding_id] = FixedWidthEncoding(width, encoding['encoding'])
        elif encoding['type'] == 'variable':
          self.encodings[encoding_id] = VariableWidthEncoding(encoding['encoding'])
        else:
          self.encodings[encoding_id] = XorEncoding(**encoding['encoding'])

    self.categories_by_name = {}
    self.categories = []

    if 'categories' in deserialized:
      for category_name, deserialized_category in deserialized['categories'].items():
        category = Category(category_name, deserialized_category, self)
        self.categories_by_name[category_name] = category
        self.categories.append(category)
    else:
      self.log.error('No categories defined')

    self.category = None


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
    self.log = logging.getLogger(__name__)
    if not deserialized:
      deserialized = {}

    if not menu:
      menu = Menu()

    self.menu = menu
    self.puzzleName = deserialized.get('puzzleName', '')

    self.clue = deserialized.get('clue', None)
    if not self.clue:
      self.clue = []

    self.init = deserialized.get('init', '')
    if not self.init:
      self.init = ''

    self.win_text = deserialized.get('winText') or ''
    if not self.win_text:
      self.win_text = ''
    self.winMessage = deserialized.get('winMessage') or []

    self.type = deserialized.get('type') or DEFAULT_PUZZLE_TYPE
    self.encoding_id = deserialized.get('encoding') or DEFAULT_ENCODING
    if self.encoding_id not in menu.encodings:
      raise MissingEncodingError(self.encoding_id, menu.encodings)

    self.encoding: BinaryEncoding = menu.encodings[self.encoding_id]
    self.win_bits = self.encoding.encode_bit_string(self.win_text)


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

  def __repr__(self):
    return '\n'.join(self.levelName)

  def go_to_next_puzzle(self):
    self.current_puzzle_index += 1
    if self.current_puzzle_index >= len(self.puzzles):
      self.current_puzzle_index = -1
    return

  def is_finished(self):
    return self.current_puzzle_index < 0

  def get_current_puzzle(self) -> Puzzle:
    """The puzzle currently being played for this level"""
    if not self.puzzles or self.current_puzzle_index >= len(self.puzzles):
      raise IndexError(f'\n{self}\nhas {len(self.puzzles)} puzzles. (Current index: {self.current_puzzle_index}.)')
    return self.puzzles[self.current_puzzle_index]


class GuessMode(Enum):
  SINGLE_BIT = 0
  SINGLE_LETTER = 1
  MULTI_BIT = 2
  TEXT = 3


class Correctness(Enum):
  INCORRECT = 0
  CORRECT = 1
  UNKNOWN = 2


class MissingEncodingError(Exception):
  def __init__(self, missing_encoding, existing_encodings=None):
    super().__init__(
      f'{missing_encoding} not found in: {existing_encodings}'
      if existing_encodings else
      f'Unsupported encoding: {missing_encoding}'
    )
    self.missing_encoding = missing_encoding
    self.existing_encodings = existing_encodings
