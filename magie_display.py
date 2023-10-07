from magie_model import Menu, Category, Puzzle, Level, GuessMode


# noinspection PyUnresolvedReferences,PyAttributeOutsideInit,DuplicatedCode
class Reference:
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


class MAGiEDisplay:
    def __init__(self):
        self.puzzle = None

    def preferred_guess_mode(self) -> GuessMode:
        pass

    def boot_up(self):
        pass

    def select_category(self, menu: Menu) -> Category:
        pass

    def select_level(self, category: Category) -> Level:
        pass

    def start_level(self, level: Level):
        pass

    def finish_level(self, level: Level):
        pass

    def navigation_menu(self, prompt, options):
        pass

    def start_puzzle(self, puzzle: Puzzle):
        pass

    def win_puzzle(self, puzzle: Puzzle):
        pass

    def guess_1_bit(self):
        pass

    def guess_bits(self, puzzle, guess_bits):
        pass

    def guess_1_char(self):
        pass

    def guess_text(self, init, win_text):
        pass

    def show_error(self, error):
        pass

    def reset(self):
        pass

