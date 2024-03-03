import time

from magie_model import Menu, Correctness, GuessMode
from magie_display import MAGiEDisplay

MENU_COMMANDS = {'B': 'GO BACK'}

TITLE_LINE = '============='
SUBTITLE_LINE = '-------------'
DEBUG = True
SYSTEM_WINDOW_HEIGHT = 4

MENU_PAUSE = 0.4
LEVEL_START_PAUSE = 0.2
WIN_PAUSE = 0.6


class Game:
    def __init__(
            self,
            menu: Menu,
            magie: MAGiEDisplay,
            guess_mode: GuessMode = None
    ):
        self.menu = menu
        self.magie = magie
        self.category = None
        self.level = None
        self.puzzle = None
        self.guess_mode = guess_mode or magie.preferred_guess_mode()
        self.on_bit_keys = ['1']
        self.off_bit_keys = ['0']

    def run(self):
        quitos_game = False

        self.magie.boot_up()

        while not quitos_game:
            quitos_category = False
            try:
                self.category = self.magie.select_category(self.menu)

                while not quitos_category:
                    selected = self.magie.select_level(self.category, MENU_COMMANDS)
                    if selected in MENU_COMMANDS:
                        quitos_category = True
                        continue

                    self.level = selected

                    self.magie.start_level(self.level)

                    time.sleep(LEVEL_START_PAUSE)
                    while not self.level.is_finished():
                        self.magie.start_puzzle(self.level.get_current_puzzle())
                        self.level.go_to_next_puzzle()

                self.magie.finish_level(self.level)

                quitos_category = self.level == self.category.levels[-1]
            except IndexError:
                self.magie.show_error([
                    "SOME KIND",
                    "OF PROBLEM",
                    "WITH THAT",
                    "LEVEL"
                ])
                continue
            except KeyboardInterrupt:
                quitos_game = True

        self.magie.quit()
