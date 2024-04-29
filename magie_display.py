from judgments import FullJudgment
from magie_model import Menu, Category, Puzzle, Level, GuessMode


class MAGiEDisplay:
    def __init__(self):
        self.puzzle = None

    def preferred_guess_mode(self) -> GuessMode:
        pass

    def boot_up(self):
        pass

    def select_category(self, menu: Menu) -> Category:
        pass

    def select_level(self, category: Category, menu_commands) -> Level:
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

    def quit(self):
        pass


class Guesser:
    def __init__(self, magie: MAGiEDisplay, puzzle: Puzzle):
        self.magie: MAGiEDisplay = magie
        self.puzzle: Puzzle = puzzle

    @classmethod
    def for_puzzle(cls, magie, puzzle: Puzzle):
        return Guesser(magie, puzzle)

    def guess(self, current_correct = None) -> FullJudgment:
        pass
