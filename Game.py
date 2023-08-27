import curses
import time

from MagieModel import Menu
from magie_display import MAGiEDisplay, ColorScheme

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'
LEVEL_START_PAUSE = 0.2
DEBUG = True
SYSTEM_WINDOW_HEIGHT = 4
MENU_PAUSE = 0.4


class Game:
    def __init__(self, menu: Menu, magie: MAGiEDisplay):
        self.menu = menu
        self.magie = magie
        self.category = None
        self.level = None
        self.puzzle = None
        self.on_bit_keys = ['1']
        self.off_bit_keys = ['0']
        self.backspace_keys = [curses.KEY_BACKSPACE, 127, 0x7f]

        self.system_window = curses.newwin(SYSTEM_WINDOW_HEIGHT, curses.COLS, curses.LINES - SYSTEM_WINDOW_HEIGHT, 0)

    def run(self):
        quitos_game = False
        quitos_level = False

        while not quitos_game:
            self.category = self.magie.select_category(self.menu)

            while not quitos_level:
                self.level = self.magie.select_level(self.category)

                self.magie.start_level(self.level)

                while not self.level.is_finished():
                    self.magie.start_puzzle(self.level.get_current_puzzle())
                    self.level.go_to_next_puzzle()

                self.magie.finish_level(self.level)

                quitos_level = True

    def start_level(self):
        self.magie.reset()

        if not self.level.puzzles:
            self.magie.show_error('No puzzles!')
            return

        self.puzzle = self.level.go_to_next_puzzle()
        self.magie.start_puzzle(self.puzzle)

        if self.level.is_finished():
            self.magie.reset()
            self.magie.title.write(self.level.levelName)
            self.magie.main.write('LEVEL FINISHED!')

        time.sleep(LEVEL_START_PAUSE)

        self.level.go_to_next_puzzle()

    def start_puzzle(self):
        self.magie.reset()
        self.magie.title.write(self.level.levelName)

        puzzle = self.level.get_current_puzzle()

        self.magie.main.write(puzzle.clue)
        self.magie.main.write(SUBTITLE_LINE)

        for c in puzzle.init:
            char_bits = puzzle.encoding.encode_bit_string(c)
            self.magie.main.write_bits(char_bits, suffix=f' {c}')

        guess_text = list(puzzle.init)
        guess_char_index = len(puzzle.init)

        while guess_text != puzzle.winText:
            self.magie.note.write(['guess text loop', f'f{puzzle.winText=}', f'{guess_text=}'])
            guess_char_bits = []

            while len(guess_char_bits) < puzzle.encoding.width:
                self.magie.note.write([f'guess bit loop', f'{puzzle.winText=}', f'{guess_text=} {guess_char_bits=}'])
                key_code = self.magie.getch()
                if key_code in self.backspace_keys:
                    self.magie.note.write(f'key code of type "{type(key_code)}": {key_code}')
                    if not guess_char_bits:
                        guess_char_index -= 1
                        guess_char = guess_text[guess_char_index]
                        guess_char_bits = list(puzzle.encoding.encode_bit_string(guess_char))
                        self.magie.back('row')
                    guess_char_bits.pop()

                else:
                    guess_bit = chr(key_code)
                    if guess_bit in self.on_bit_keys:
                        guess_bit = '1'
                    elif guess_bit in self.off_bit_keys:
                        guess_bit = '0'
                    else:
                        continue
                    guess_char_bits += [guess_bit]

                bit_colors = [self.magie.colors.unknown] * len(guess_char_bits)

                if guess_char_index < len(puzzle.winText):
                    win_char = puzzle.winText[guess_char_index]
                    win_char_bits = list(puzzle.encoding.encode_bit_string(win_char))

                    for i in range(min(len(guess_char_bits), len(win_char_bits))):
                        if guess_char_bits[i] == win_char_bits[i]:
                            bit_colors[i] = self.magie.colors.correct
                        else:
                            bit_colors[i] = self.magie.colors.incorrect

                    guess_char = puzzle.encoding.decode_bit_string(guess_char_bits)
                    padding = 1 + puzzle.encoding.width - len(guess_char_bits)
                    self.magie.main.write_bits(guess_char_bits, bit_colors, suffix=f' {guess_char:>{padding}}', stay_on_line=True)

                    if guess_char == win_char:
                        if guess_char_index >= len(guess_text):
                            guess_text.append(guess_char)
                        else:
                            guess_text[guess_char_index] = guess_char
                        self.magie.main.advance_guess_char()
                        guess_char_index += 1

        self.magie.main.write(puzzle.winMessage)
        self.magie.getch()
