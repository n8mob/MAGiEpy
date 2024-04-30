import unittest
from unittest.mock import Mock

from magie_model import Puzzle, MissingEncodingError


class PuzzleTests(unittest.TestCase):
  def test_initWithNoArgs(self):
    try:
      _ = Puzzle()
    except MissingEncodingError as missing:
      self.assertIn('encoding', str(missing))

  def test_initWithEmptyArgs(self):
    menu = Mock()
    menu.encodings = {}

    try:
      _ = Puzzle({'clue': [], 'winText': '', 'init': ''}, menu)
    except MissingEncodingError as missing:
      self.assertIn('encoding', str(missing))

  def test_initWithNoneArgs(self):
    try:
      _ = Puzzle({'clue': None, 'winText': None, 'init': None}, None)
    except MissingEncodingError as missing:
      self.assertIn('encoding', str(missing))
