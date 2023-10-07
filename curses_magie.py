import curses

from game import Game
from magie_display import MAGiEDisplay
from magie_model import Menu, Category, Level, Puzzle

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'

class ColorScheme:
    default = None

    def __init__(self, correct, incorrect, unknown, error):
        self.correct = correct
        self.incorrect = incorrect
        self.unknown = unknown
        self.error = error

    @classmethod
    def default_color_scheme(cls):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_YELLOW)

        if not cls.default:
            cls.default = ColorScheme(
                curses.color_pair(1) | curses.A_BOLD,
                curses.color_pair(2) | curses.A_BOLD,
                curses.color_pair(3) | curses.A_BOLD,
                curses.color_pair(4)
            )

        return cls.default

class MagieWindow:
    def __init__(self,
                 window: curses.window,
                 colors: ColorScheme,
                 height,
                 width,
                 default_bit='0',
                 title_line=None,
                 auto_clear=False):
        self.window = window
        self.colors = colors
        self.height = height
        self.width = width
        self.y = 0
        self.x = 0
        self.default_bit = default_bit
        self.title_line = title_line
        self.auto_clear = auto_clear

    def reset(self):
        self.y = 0
        self.x = 0
        self.window.clear()

    def write(self, lines, prefix=''):
        if self.auto_clear:
            self.reset()

        if isinstance(lines, str):
            lines = lines.split('\n')

        x = self.x

        if prefix:
            self.window.addstr(self.y, x, prefix)
            x = len(prefix) + 1

        for line in lines:
            self.window.addstr(self.y, x, line)
            self.y += 1

        if self.title_line:
            self.window.addstr(self.y, self.x, self.title_line)
            self.y += 1

        self.window.refresh()

    def write_bits(self, bits=None, bit_colors=None, stay_on_line=False, prefix='  ', suffix=' ', bit_width=None):
        if not bits:
            bits = [self.default_bit] * (bit_width or self.width)

        bit_x = self.x
        known_bit_colors = bit_colors or []

        if len(known_bit_colors) < len(bits):
            known_bit_colors += [self.colors.unknown] * (len(bits) - len(known_bit_colors))

        self.window.addstr(self.y, bit_x, prefix)
        bit_x += len(prefix)

        for i in range(len(bits)):
            if self.y >= self.height or self.x >= self.width:
                raise IndexError(f"Seems like we're off the end of the display: {self.describe_state()}")
            try:
                self.window.addch(self.y, bit_x + i, bits[i], known_bit_colors[i])
            except curses.error as cerror:
                raise RuntimeError(
                    f"Unknown error writing bit '{bits[i]}' at column {bit_x} ( {self.describe_state()} )", cerror)

        self.window.addstr(self.y, bit_x + len(bits), suffix)

        if not stay_on_line:
            self.advance_guess_char()

    def advance_guess_char(self):
        self.y += 1

    def reverse_guess_char(self):
        self.y -= 1

    def describe_state(self):
        return f"{self.y=}, {self.height=}, {self.x=}, {self.width=}"


class CursesMAGiE(MAGiEDisplay):
    def __init__(self,
                 scr: curses.window,
                 colors: ColorScheme,
                 default_bit='0',
                 title_height=4,
                 note_height=4,
                 display_width=None):
        super().__init__()
        self.full_screen = scr
        self.default_bit = default_bit
        self.colors = colors
        self.display_width = display_width or curses.COLS

        puzzle_display_height = curses.LINES - (title_height + note_height)

        self.title = MagieWindow(
            curses.newwin(title_height, self.display_width, 0, 0),
            colors,
            title_height,
            self.display_width,
            title_line=TITLE_LINE
        )
        self.main = MagieWindow(
            curses.newwin(puzzle_display_height, self.display_width, title_height, 0),
            colors,
            puzzle_display_height,
            self.display_width
        )
        self.note = MagieWindow(
            curses.newwin(note_height, self.display_width, curses.LINES - note_height, 0),
            colors,
            note_height,
            self.display_width,
            auto_clear=True
        )

    def select_category(self, menu: Menu) -> Category:
        self.reset()
        self.title.write(['CHOOSOS', 'CATEGORY'])

        for index, category in enumerate(menu.categories):
            self.main.write(category.name, f'{index}: ')

        category_number = int(chr(self.getch()))
        return menu.categories[category_number]

    def select_level(self, category: Category) -> Level:
        self.reset()
        self.title.write(category.name)
        self.main.write(['SELECTOS', 'LEVEL', SUBTITLE_LINE])

        for index, level in enumerate(category.levels):
            self.main.write(level.levelName, f'{index}: ')

        level_number = int(self.getkey())
        return category.levels[level_number]

    def start_level(self, level: Level):
        if not level.puzzles:
            self.note.write('No puzzles!')
            return
        else:
            self.title.write(level.levelName)

        level.go_to_next_puzzle()

    def finish_level(self, level: Level):
        self.main.write([SUBTITLE_LINE, '', 'GOOD WORK!', 'YOU FINISHOS', 'LEVEL', ''] + level.levelName)

    def start_puzzle(self, puzzle: Puzzle):
        self.main.reset()
        self.main.write(puzzle.clue)
        self.main.write(SUBTITLE_LINE)

        for c in puzzle.init:
            char_bits = puzzle.encoding.encode_bit_string(c)
            self.main.write_bits(char_bits, suffix=f' {c}')


    def reset(self):
        self.main.reset()
        self.title.reset()
        self.note.reset()

    def getch(self):
        return self.main.window.getch()

    def getkey(self):
        return self.main.window.getkey()

    def back(self, distance):
        if 'row' == distance:
            self.main.y -= 1
        if 'char' == distance:
            self.main.x -= 1
        self.main.window.refresh()


def start_game(scr: curses.window, json_path):
    with open(json_path) as menu_file:
        menu = Menu(file=menu_file)

    magie = CursesMAGiE(scr, ColorScheme.default_color_scheme())

    game = Game(menu, magie)
    game.run()


if __name__ == '__main__':
    curses.wrapper(start_game, 'TestMenus/FullMenu.json')
