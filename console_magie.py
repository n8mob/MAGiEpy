from game import Game
from magie_display import MAGiEDisplay, TITLE_LINE
from magie_model import Menu, Category, Puzzle, Level, GuessMode


class ConsoleMAGiE(MAGiEDisplay):
    def __init__(self):
        super().__init__()
        self.on_bits = ['1']
        self.off_bits = ['0']
        self.ignore = [' ', ',', '_']

        self.decode_bits = ['0', '1', '?']
        self.incorrect_bits = {'0': '⓿', '1': '➊'}
        self.correct_bits = {'0': '0', '1': '1'}

    def preferred_guess_mode(self) -> GuessMode:
        return GuessMode.MULTI_BIT

    def out(self, text=''):
        print(self.prep(text))

    def read(self, prompt='', include_prompt=False):
        prompt = self.prep(prompt)
        _input = self.prep(input(prompt))
        if include_prompt:
            return prompt + _input
        else:
            return _input

    @staticmethod
    def prep(text):
        u = ''.join((c.lower() if c in ['i', 'I'] else c.upper() for c in text))
        return u

    def judge_bitstring(self, guess, win):
        max_possible = min(len(guess), len(win))
        is_correct = max_possible > 0
        judged = ''

        for i in range(max_possible):
            is_correct = is_correct and guess[i] == win[i]
            if guess[i] == win[i]:
                judged += self.correct_bits[guess[i]]
            else:
                judged += self.incorrect_bits[guess[i]]

        return is_correct, judged

    def get_judgement_display(self, judgment):
        """Return a string of bits, decorated according to their correctness, ready to display"""
        judged = ''

        for i in range(len(judgment)):
            if judgment[i] in self.on_bits:
                judged += self.correct_bits[judgment[i]]
            else:
                judged += self.incorrect_bits[judgment[i]]

        return judged

    def boot_up(self):
        self.out('welcome to MAGiE')
        self.out(TITLE_LINE)
        self.out()

    def show_error(self, error):
        self.out(error)

    def select_category(self, menu: Menu):
        for i, category in enumerate(menu.categories):
            self.out(f'{i:>2} {category.name}')

        category_number = int(input('select category: '))

        return menu.categories[category_number]

    def select_level(self, category: Category):
        for i, level in enumerate(category.levels):
            pre = f'{i:>2}'
            for line in level.levelName:
                self.out(f'{pre} {line}')
                pre = ' ' * len(pre)

        level_number = int(input('select level: '))

        return category.levels[level_number]

    def start_level(self, level: Level):
        level.current_puzzle_index = 0

    def start_puzzle(self, puzzle: Puzzle):
        for line in puzzle.clue:
            self.out(line)

        self.out(puzzle.init)

    def win_puzzle(self, puzzle: Puzzle):
        self.out(puzzle.win_text)
        self.out(TITLE_LINE)
        for line in puzzle.winMessage:
            self.out(line)
        self.out(TITLE_LINE)

    def guess_1_bit(self):
        return input()

    def guess_bits(self, puzzle, guess_bits):
        if not guess_bits:
            guess_bits = puzzle.encoding.encode_bit_string(puzzle.init)

        _input = input(guess_bits)

        for b in _input:
            if b in self.on_bits:
                guess_bits += '1'
            elif b in self.off_bits:
                guess_bits += '0'
            else:
                continue  # skip invalid bits
                # we could skip self.ignore and throw on others, if we want

        all_correct, correct_guess_chars, judgements = puzzle.judge(guess_bits)

        for i, char_judgement in enumerate(judgements):
            judged_bits = self.get_judgement_display(char_judgement[1])
            self.out(puzzle.encoding.decode_bit_string(correct_guess_chars[i]) + ' ' + judged_bits)

        return guess_bits

    def guess_1_char(self):
        return input()

    def guess_text(self, init, win_text):
        win_text = self.prep(win_text)
        guess_text = self.read(init, include_prompt=True)
        max_check = min(len(guess_text), len(win_text))
        correct_guesses = ''
        for i in range(max_check):
            if guess_text[i] == win_text[i]:
                correct_guesses += win_text[i]
            else:
                break
        self.out(correct_guesses)
        return correct_guesses.rstrip().upper()

    def reset(self):
        pass


def start_game(json_path):
    with open(json_path) as menu_file:
        menu = Menu(file=menu_file)

    magie = ConsoleMAGiE()

    game = Game(menu, magie)
    game.run()


if __name__ == '__main__':
    start_game('TestMenus/FullMenu.json')
