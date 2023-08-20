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

    def write_bit_char(self, char_bits, bit_colors=None, prefix='  ', suffix=' ', ):
        bit_x = self.xq

        if not bit_colors:
            bit_colors =  [self.unknown_color] * len(char_bits)
        elif len(bit_colors) < len(char_bits):
            bit_colors += [self.unknown_color] * (len(char_bits) - len(bit_colors))

        self.scr.addstr(self.y, bit_x, prefix)
        bit_x += len(prefix)

        for i in range(len(char_bits)):
            self.scr.addch(self.y, bit_x + i, char_bits[i], bit_colors[i])

        self.scr.addstr(self.y, bit_x + len(char_bits), suffix)
        self.y += 1

    def write_plain_bit_string(self, s, encoding: BinaryEncoding, left_padding='  ', right_padding=' '):
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
        level_number = int(self.scr.getkey())
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

        for c in puzzle.init:
            char_bits = puzzle.encoding.encode_bit_string(c)
            self.write_bit_char(char_bits, suffix=f' {c}')

        guess_char_index = len(puzzle.init)

        while not puzzle.isSolved:
            guess_char = self.scr.getkey().upper()
            win_char = puzzle.winText[guess_char_index]
            guess_char_bits = puzzle.encoding.encode_bit_string(guess_char)
            win_char_bits = puzzle.encoding.encode_bit_string(win_char)
            bit_colors = [self.unknown_color] * len(puzzle.encoding.encode_bit_string(guess_char))

            for i in range(len(guess_char_bits)):
                if guess_char_bits[i] == win_char_bits[i]:
                    bit_colors[i] = self.correct_color
                else:
                    bit_colors[i] = self.incorrect_color

            self.write_bit_char(puzzle.encoding.encode_bit_string(guess_char), bit_colors, suffix=f' {guess_char}')
            if guess_char == win_char:
                guess_char_index += 1
                puzzle.isSolved = guess_char_index >= len(puzzle.winText)
            else:
                self.y -= 1

        self.x = 0
        self.y += 1
        self.write_text(puzzle.winMessage)
        self.scr.getch(self.y, self.x)
