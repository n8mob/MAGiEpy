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
        self.assertEqual(len(actual_menu.categories), 1)

        actual_category = actual_menu.categories[0]
        self.assertIsNotNone(actual_category)
        self.assertEqual('only', actual_category.name)
        self.assertIsNotNone(actual_category.levels)
        self.assertEqual(len(actual_category.levels), 1)

        actual_level = actual_category.levels[0]

        self.assertIsNotNone(actual_level)
        self.assertEqual(['THIS IS THE', 'ONLY LEVEL'], actual_level.levelName)

        self.assertIsNotNone(actual_level.puzzles)
        self.assertEqual(len(actual_level.puzzles), 1)

        actual_puzzle = actual_level.puzzles[0]

        self.assertIsNotNone(actual_puzzle)
        self.assertEqual(actual_puzzle.puzzleName, 'Only Puzzle')
        self.assertEqual(actual_puzzle.init, '')
        self.assertEqual(actual_puzzle.winText, 'WIN')
        self.assertEqual(actual_puzzle.clue, ['TRY TO', 'WIN'])
        self.assertEqual(actual_puzzle.winMessage, ['YOU', 'WIN!'])

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
        actual = Level()
        self.assertEqual([], actual.levelName)
        self.assertEqual([], actual.puzzles)


class PuzzleTests(unittest.TestCase):
    def test_initWithNoArgs(self):
        actual = Puzzle()

        self.assertEqual([], actual.clue)
        self.assertEqual('', actual.winText)
        self.assertEqual('', actual.init)

    def test_initWithEmptyArgs(self):
        actual = Puzzle({'clue': [], 'winText': '', 'init': ''})

        self.assertEqual([], actual.clue)
        self.assertEqual('', actual.winText)
        self.assertEqual('', actual.init)

    def test_initWithEmptyStrings(self):
        actual = Puzzle({'clue': '', 'winText': '', 'init': ''})

        self.assertEqual([], actual.clue)
        self.assertEqual('', actual.winText)
        self.assertEqual('', actual.init)

    def test_initWithNoneArgs(self):
        actual = Puzzle({'clue': None, 'winText': None, 'init': None})

        self.assertEqual([], actual.clue, [])
        self.assertEqual('', actual.winText)
        self.assertEqual('', actual.init)


if __name__ == '__main__':
    unittest.main()
