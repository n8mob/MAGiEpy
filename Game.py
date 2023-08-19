import curses
import time

from MagieModel import Menu
from Encodings import BinaryEncoding

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'
LEVEL_START_PAUSE = 0.2


class Game:
    def __init__(self, scr: curses.window, menu: Menu):
        self.scr = scr
        self.y = 0
        self.x = 0
        self.menu = menu
        self.category = None
        self.level = None

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.incorrect_color = curses.color_pair(1) | curses.A_BOLD
        self.correct_color = curses.color_pair(2) | curses.A_BOLD
        self.unknown_color = curses.color_pair(3) | curses.A_BOLD

    def reset(self):
        self.y = 0
        self.x = 0
        self.scr.clear()

    def write_text(self, lines, indicator=''):
        if isinstance(lines, str):
            lines = lines.split('\n')

        if indicator:
            self.scr.addstr(self.y, self.x, indicator)
            self.x = len(indicator) + 1

        for line in lines:
            self.scr.addstr(self.y, self.x, line)
            self.y += 1

        self.x = 0

    def write_bits(self, s, encoding: BinaryEncoding, left_padding='  ', right_padding=' '):

        for c in s:
            bits = encoding.encode_bit_string(c)
            self.write_text(bits + right_padding + c, left_padding)

    def choose_category(self):
        self.reset()

        for index, category in enumerate(self.menu.categories):
            self.write_text(category.name, f'{index}: ')

        self.y += 1

        self.write_text('select category: ')
        category_number = int(chr(self.scr.getch()))
        self.category = self.menu.categories[category_number]

    def choose_level(self):
        self.reset()

        self.write_text([self.category.name, TITLE_LINE])

        self.y += 1

        for index, level in enumerate(self.category.levels):
            self.write_text(level.levelName, f'{index}: ')

        self.y += 1

        self.write_text('select level: ')
        level_number = int(chr(self.scr.getch()))
        self.level = self.category.levels[level_number]

    def start_level(self):
        self.reset()

        if not self.level.puzzles:
            self.write_text('No puzzles!')
            return

        if self.level.is_finished():
            self.reset()
            self.write_text(self.level.levelName)
            self.y += 1
            self.write_text('LEVEL FINISHED!')

        time.sleep(LEVEL_START_PAUSE)

        self.level.go_to_next_puzzle()

    def start_puzzle(self):
        self.reset()
        self.write_text(self.level.levelName)
        self.write_text(TITLE_LINE)

        self.y += 1

        puzzle = self.level.get_current_puzzle()

        self.write_text(puzzle.clue)
        self.write_text(SUBTITLE_LINE)
        self.y += 1

        self.write_bits(puzzle.init, puzzle.encoding)

        guess_char_index = len(puzzle.init)

        while not puzzle.isSolved:
            self.x = guess_char_index
            guess_char = chr(int(self.scr.getch(self.y, guess_char_index))).upper()
            win_char = puzzle.winText[guess_char_index]
            if guess_char == win_char:
                self.scr.addch(self.y, guess_char_index, guess_char, self.correct_color)
                self.scr.addstr(self.y + 1, 0, puzzle.encoding.encode_bit_string(guess_char), self.correct_color)
                guess_char_index += 1
                puzzle.isSolved = guess_char_index >= len(puzzle.winText)
            else:
                self.scr.addch(self.y, guess_char_index, guess_char, self.incorrect_color)
                guess_char_bits = puzzle.encoding.encode_bit_string(guess_char)
                win_char_bits = puzzle.encoding.encode_bit_string(win_char)

                for i, bit_x in enumerate(range(2, puzzle.encoding.width + 2)):
                    guess_bit = guess_char_bits[i]
                    win_bit = win_char_bits[i]
                    correctness = self.correct_color if guess_bit == win_bit else self.incorrect_color
                    self.scr.addch(self.y + 1, bit_x, guess_bit, correctness)

        self.x = 0
        self.y += 1
        self.write_text(puzzle.winMessage)
        self.scr.getch(self.y, self.x)
