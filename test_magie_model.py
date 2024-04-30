import json
import unittest

from magie_model import Level, Menu


class MenuTest(unittest.TestCase):
  def test_BasicJson(self):
    with open('TestMenus/MinimalMenu.json') as minimal_file:
      serialized = minimal_file.read()

    self.assertGreaterEqual(len(serialized), 30)
    plain_json = json.loads(serialized)

    self.assertIsNotNone(plain_json)
    self.assertIsNotNone(plain_json['menuVersion'])
    self.assertEqual(plain_json['menuVersion'], 1)
    self.assertIsNotNone(plain_json['categories'])

    actual_menu = Menu(serialized=serialized)

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
    self.assertEqual(actual_puzzle.win_text, '_ABCDEFG')
    self.assertEqual(actual_puzzle.clue, ['CONTINUE', 'THE PATTERN'])
    self.assertEqual(actual_puzzle.winMessage, ['THAT IS', 'CORRECT!'])

  def test_fullMenu(self):
    with open('TestMenus/BigGame.json') as full_file:
      full_menu = Menu(file=full_file)

    self.assertIsNotNone(full_menu)
    self.assertEqual(7, len(full_menu.categories))

    expected_categories = [
      'quick alpha',
      'quick fixed',
      'stories',
      'at the mall',
      'TEDIUM',
      'ALPHA LENGTH ENCODING',
      'FIVE BIT A1  ENCODING'
    ]

    self.assertEqual(expected_categories, [cat.name for cat in full_menu.categories])

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


if __name__ == '__main__':
  unittest.main()
