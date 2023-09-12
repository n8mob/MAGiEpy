import curses
import time

from magie_model import Menu, Correctness, GuessMode
from magie_display import MAGiEDisplay, ColorScheme

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'
DEBUG = True
SYSTEM_WINDOW_HEIGHT = 4

MENU_PAUSE = 0.4
LEVEL_START_PAUSE = 0.2
WIN_PAUSE = 0.6


class Game:
    def __init__(self, menu: Menu, magie: MAGiEDisplay, guess_mode: GuessMode=None):
        self.menu = menu
        self.magie = magie
        self.category = None
        self.level = None
        self.puzzle = None
        self.guess_mode = guess_mode or magie.preferred_guess_mode()
        self.on_bit_keys = ['1']
        self.off_bit_keys = ['0']
        self.backspace_keys = [curses.KEY_BACKSPACE, 127, 0x7f]

    def run(self):
        quitos_game = False
        quitos_level = False

        self.magie.boot_up()

        while not quitos_game:
            self.category = self.magie.select_category(self.menu)

            while not quitos_level:
                self.level = self.magie.select_level(self.category)

                self.magie.start_level(self.level)

                time.sleep(LEVEL_START_PAUSE)

                while not self.level.is_finished():
                    self.start_puzzle(self.level.get_current_puzzle())

                    self.level.go_to_next_puzzle()

                self.magie.finish_level(self.level)

                quitos_level = True

    def start_puzzle(self, puzzle):
        self.magie.start_puzzle(puzzle)

        guess_text = puzzle.init
        guess_char_index = 0

        while guess_text != puzzle.win_text:
            if self.guess_mode == GuessMode.MULTI_BIT:
                guess_bits = puzzle.encoding.encode_bit_string(guess_text)
                guess_bits = self.magie.guess_bits(puzzle, guess_bits)
                guess_text = puzzle.encoding.decode_bit_string(guess_bits)

            elif self.guess_mode == GuessMode.SINGLE_BIT:
                guess_char_bits = []
                while len(guess_char_bits) < puzzle.encoding.width:
                    guess_bit = self.magie.guess_1_bit()
                    if guess_bit in self.on_bit_keys:
                        guess_bit = '1'
                    elif guess_bit in self.off_bit_keys:
                        guess_bit = '0'
                    else:
                        continue
                    guess_char_bits += [guess_bit]

                    bit_correctnesses = ['?' for bit in guess_char_bits]

                    if guess_char_index < len(puzzle.win_text):
                        win_char = puzzle.win_text[guess_char_index]
                        win_char_bits = list(puzzle.encoding.encode_bit_string(win_char))

                        for i in range(min(len(guess_char_bits), len(win_char_bits))):
                            if guess_char_bits[i] == win_char_bits[i]:
                                bit_correctnesses[i] = '1'
                            else:
                                bit_correctnesses[i] = '0'

                        guess_char = puzzle.encoding.decode_bit_string(guess_char_bits)

                        if guess_char == win_char:
                            if guess_char_index >= len(guess_text):
                                guess_text.append(guess_char)
                            else:
                                guess_text[guess_char_index] = guess_char
                            guess_char_index += 1
            elif self.guess_mode == GuessMode.TEXT:
                if guess_text:
                    guess_text = self.magie.guess_text(guess_text, puzzle.win_text)
                else:
                    guess_text = self.magie.guess_text(puzzle.init, puzzle.win_text)

        self.magie.win_puzzle(puzzle)
        time.sleep(WIN_PAUSE)
