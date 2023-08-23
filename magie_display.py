import curses

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'


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
    def __init__(self, window, colors: ColorScheme, height, width, default_bit='0', title_line=None):
        self.window = window
        self.colors = colors
        self.height = height
        self.width = width
        self.y = 0
        self.x = 0
        self.default_bit = default_bit
        self.title_line = title_line

    def reset(self):
        self.y = 0
        self.x = 0
        self.window.clear()

    def write(self, lines, prefix=''):
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
            self.window.addstr(self.y, x, TITLE_LINE)
            self.y += 1

    def write_bits(self, bits=None, bit_colors=None, prefix='  ', suffix=' ', bit_width=13):
        if not bits:
            bits = [self.default_bit] * bit_width

        bit_x = self.x
        known_bit_colors = bit_colors or []

        if len(known_bit_colors) < len(bits):
            known_bit_colors += [self.colors.unknown] * (len(bits) - len(known_bit_colors))

        self.window.addstr(self.y, bit_x, prefix)
        bit_x += len(prefix)

        for i in range(len(bits)):
            self.window.addch(self.y, bit_x + i, bits[i], known_bit_colors[i])

        self.window.addstr(self.y, bit_x + len(bits), suffix)
        self.y += 1

class MagieDisplay:
    def __init__(self, scr: curses.window, colors: ColorScheme, default_bit='0', title_height=4, note_height=4):
        self.full_screen = scr
        self.default_bit = default_bit
        self.colors = colors

        puzzle_display_height = curses.LINES - (title_height + note_height)

        self.title = MagieWindow(
            curses.newwin(title_height, curses.COLS, 0, 0),
            colors,
            title_height,
            curses.COLS,
            title_line=TITLE_LINE
        )
        self.note = MagieWindow(
            curses.newwin(note_height, curses.COLS, curses.LINES - note_height, 0),
            colors,
            note_height,
            curses.COLS
        )
        self.main = MagieWindow(
            curses.newwin(puzzle_display_height, curses.COLS, title_height, 0),
            colors,
            puzzle_display_height,
            curses.COLS
        )

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