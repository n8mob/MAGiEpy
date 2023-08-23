import curses
import time

from MagieModel import Menu

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'
LEVEL_START_PAUSE = 0.2
DEBUG = False

class Game:
    def __init__(self, scr: curses.window, menu: Menu):
        self.scr = scr
        self.y = 0
        self.x = 0
        self.menu = menu
        self.category = None
        self.level = None
        self.on_bit_keys = ['1']
        self.off_bit_keys = ['0']
        self.backspace_keys = [curses.KEY_BACKSPACE, 127, 0x7f]
        self.system_window = scr

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_YELLOW)

        self.incorrect_color = curses.color_pair(1) | curses.A_BOLD
        self.correct_color = curses.color_pair(2) | curses.A_BOLD
        self.unknown_color = curses.color_pair(3) | curses.A_BOLD
        self.error_color = curses.color_pair(4)

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

    def write_bits(self, char_bits=None, bit_colors=None, prefix='  ', suffix=' '):
        if not char_bits:
            char_bits = []

        bit_x = self.x
        known_bit_colors = bit_colors or []

        if len(known_bit_colors) < len(char_bits):
            known_bit_colors += [self.unknown_color] * (len(char_bits) - len(known_bit_colors))

        self.scr.addstr(self.y, bit_x, prefix)
        bit_x += len(prefix)

        for i in range(len(char_bits)):
            self.scr.addch(self.y, bit_x + i, char_bits[i], known_bit_colors[i])

        self.scr.addstr(self.y, bit_x + len(char_bits), suffix)

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
            self.write_bits(char_bits, suffix=f' {c}')
            self.y += 1

        guess_text = list(puzzle.init)
        guess_char_index = len(puzzle.init)

        while guess_text != puzzle.winText:
            win_char = puzzle.winText[guess_char_index]
            win_char_bits = list(puzzle.encoding.encode_bit_string(win_char))
            guess_char = None
            guess_char_bits = []

            while len(guess_char_bits) < puzzle.encoding.width:
                key_code = self.scr.getch()
                if key_code in self.backspace_keys:
                    if DEBUG:
                        self.system_window.addstr(self.y + 1, self.x + 5, f'key code of type "{type(key_code)}": {key_code}')
                    if guess_char_bits:
                        guess_char_bits.pop()
                    else:
                        guess_char_index -= 1
                        guess_char = guess_text[guess_char_index]
                        guess_char_bits = list(puzzle.encoding.encode_bit_string(guess_char))
                        self.y -= 1
                    self.scr.refresh()
                else:
                    guess_bit = chr(key_code)
                    if guess_bit in self.on_bit_keys:
                        guess_bit = '1'
                    elif guess_bit in self.off_bit_keys:
                        guess_bit = '0'
                    else:
                        continue
                    guess_char_bits += [guess_bit]

                bit_colors = [self.unknown_color] * puzzle.encoding.width

                for i in range(len(guess_char_bits)):
                    if guess_char_bits[i] == win_char_bits[i]:
                        bit_colors[i] = self.correct_color
                    else:
                        bit_colors[i] = self.incorrect_color

                guess_char = puzzle.encoding.decode_bit_string(guess_char_bits)
                padding = 1 + puzzle.encoding.width - len(guess_char_bits)
                self.write_bits(guess_char_bits, bit_colors, suffix=f' {guess_char:>{padding}}')

            if guess_char == win_char:
                if guess_char_index <= len(guess_text):
                    guess_text.append(guess_char)
                else:
                    guess_text[guess_char_index] = guess_char
                guess_char_index += 1
                self.y += 1
            else:
                guess_char_bits.clear()

        self.x = 0
        self.y += 1
        self.write_text(puzzle.winMessage)
        self.scr.getch(self.y, self.x)
