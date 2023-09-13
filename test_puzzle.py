import unittest
from unittest.mock import Mock

from magie_model import Puzzle


class PuzzleTests(unittest.TestCase):
    def test_initWithNoArgs(self):
        try:
            _ = Puzzle()
        except ValueError as ve:
            self.assertIn('encoding', str(ve))

    def test_initWithEmptyArgs(self):
        menu = Mock()
        menu.encodings = {}

        try:
            _ = Puzzle({'clue': [], 'winText': '', 'init': ''}, menu)
        except ValueError as ve:
            self.assertIn('encoding', str(ve))

    def test_initWithNoneArgs(self):
        try:
            _ = Puzzle({'clue': None, 'winText': None, 'init': None}, None)
        except ValueError as ve:
            self.assertIn('encoding', str(ve))
