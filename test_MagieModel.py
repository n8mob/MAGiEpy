import json
import unittest
from unittest.mock import Mock

from magiegame.MagieModel import Level, Menu, Puzzle


class MenuTest(unittest.TestCase):
    def setUp(self) -> None:
        self.screen = Mock()

    def test_BasicJson(self):
        with open('TestMenus/MinimalMenu.json') as minimal_file:
            serialized = minimal_file.read()

        self.assertGreaterEqual(len(serialized), 30)
        plain_json = json.loads(serialized)

        self.assertIsNotNone(plain_json)
        self.assertIsNotNone(plain_json['menuVersion'])
        self.assertEqual(plain_json['menuVersion'], 1)
        self.assertIsNotNone(plain_json['categories'])

        actual_menu = Menu(self.screen, serialized)

        self.assertIsNotNone(actual_menu)
        self.assertIsNotNone(actual_menu.categories)
        self.assertEqual(len(actual_menu.categories), 2)

        self.assertIn('tests', actual_menu.categories_by_name)
        self.assertIn('other', actual_menu.categories_by_name)

        actual_category = actual_menu.categories_by_name['other']
        self.assertIsNotNone(actual_category)
        self.assertEqual('other', actual_category.name)
        self.assertIsNotNone(actual_category.levels)
        self.assertEqual(len(actual_category.levels), 1)

        actual_level = actual_category.levels[0]

        self.assertIsNotNone(actual_level)
        self.assertEqual(['THIS IS THE', 'FIRST LEVEL'], actual_level.levelName)

        self.assertIsNotNone(actual_level.puzzles)
        self.assertEqual(len(actual_level.puzzles), 2)

        actual_puzzle = actual_level.puzzles[0]

        self.assertIsNotNone(actual_puzzle)
        self.assertEqual(actual_puzzle.puzzleName, 'Initial')
        self.assertEqual(actual_puzzle.init, '_ABCD')
        self.assertEqual(actual_puzzle.winText, '_ABCDEFG')
        self.assertEqual(actual_puzzle.clue, ['CONTINUE', 'THE PATTERN'])
        self.assertEqual(actual_puzzle.winMessage, ['THAT IS', 'CORRECT!'])

    def test_fullMenu(self):
        with open('TestMenus/FullMenu.json') as full_file:
            full_menu = Menu(self.screen, file=full_file)

        self.assertIsNotNone(full_menu)
        self.assertEqual(5, len(full_menu.categories))

        self.assertEqual('stories', full_menu.categories[0].name)
        self.assertEqual('at the mall', full_menu.categories[1].name)
        self.assertEqual('TEDIUM', full_menu.categories[2].name)
        self.assertEqual('ALPHA LENGTH ENCODING', full_menu.categories[3].name)
        self.assertEqual('FIVE BIT A1  ENCODING', full_menu.categories[4].name)

        at_the_mall = full_menu.categories_by_name['at the mall']
        self.assertEqual(len(at_the_mall.levels), 7)

        for level in at_the_mall.levels:
            self.assertIsNotNone(level.levelName)
            self.assertGreaterEqual(len(level.levelName), 1)
            self.assertIsNotNone(level.puzzles)
            num_puzzles = len(level.puzzles)
            self.assertGreaterEqual(num_puzzles, 6, f'level "{level.levelName}" only has {num_puzzles} puzzles')


class LevelTests(unittest.TestCase):
    def test_NoArgInit(self):
        try:
            actual = Level()
        except TypeError as t:
            self.assertIn('encodings', str(t))


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


if __name__ == '__main__':
    unittest.main()
