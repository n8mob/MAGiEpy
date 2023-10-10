from game import Game
from judgments import FullJudgment, CharJudgment
from magie_display import MAGiEDisplay, Guesser
from magie_model import Menu, Category, Puzzle, Level, GuessMode

THANK_YOU_FOR_PLAYOS = ['THANK YOU', 'FOR PLAYOS', 'MAGiE']

TITLE_LINE = '============='


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

    def finish_level(self, level: Level):
        self.out('GOOD WORK!')
        self.out('YOU FINISHOS')
        self.out('THE LEVEL')
        for line in level.levelName:
            self.out(line)
        self.out(TITLE_LINE)
        self.out('')

    def start_puzzle(self, puzzle: Puzzle):
        for line in puzzle.clue:
            self.out(line)

        guesser = self.guesser(puzzle)
        judgment = guesser.guess()

        while not judgment.correct:
            judgment = guesser.guess(judgment.correct_guess)

        self.win_puzzle(puzzle)

    def guesser(self, puzzle):
        if puzzle.type == 'Decode':
            return ConsoleDecodingGuesser(self, puzzle)
        else:
            return ConsoleEncodingGuesser(self, puzzle)

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

    def win_puzzle(self, puzzle: Puzzle):
        self.out(puzzle.win_text)
        self.out(TITLE_LINE)
        for line in puzzle.winMessage:
            self.out(line)
        self.out(TITLE_LINE)

    def reset(self):
        pass

    def quit(self, quit_message = None):
        if not quit_message:
            quit_message = THANK_YOU_FOR_PLAYOS
        elif isinstance(quit_message, str):
            quit_message = [quit_message]

        self.out('')
        self.out(TITLE_LINE)
        for line in quit_message:
            self.out(line)


class ConsoleGuesser(Guesser):
    def __init__(self, magie: ConsoleMAGiE, puzzle):
        super().__init__(magie, puzzle)
        self.magie: ConsoleMAGiE = magie


class ConsoleEncodingGuesser(ConsoleGuesser):
    def guess(self, current_correct=None) -> FullJudgment:
        if not current_correct:
            current_correct = self.puzzle.encoding.encode_bit_string(self.puzzle.init)

        _input = input(current_correct)

        guess_bits = ''

        for b in _input:
            if b in self.magie.on_bits:
                guess_bits += '1'
            elif b in self.magie.off_bits:
                guess_bits += '0'
            else:
                continue  # skip invalid bits
                # we could skip self.ignore and throw on others, if we want

        full_judgment: FullJudgment = self.puzzle.encoding.judge_bits(guess_bits)

        for i, char_judgment in enumerate(full_judgment.char_judgments):
            judged_bits_display = self.get_judgment_display(char_judgment)
            self.magie.out(self.puzzle.encoding.decode_bit_string(char_judgment.guess) + ' ' + judged_bits_display)

        return full_judgment

    def get_judgment_display(self, char_judgement: CharJudgment):
        """Return a string of bits, decorated according to their correctness, ready to display"""
        judged = ''

        for i, bit_judgment in enumerate(char_judgement.judgment):
            if i < len(char_judgement.guess):
                guessed_bit = char_judgement.judgment[i]
            else:
                guessed_bit = '0'

            if bit_judgment in self.magie.on_bits:  # judgment indicates a correct bit
                judged += self.magie.correct_bits[guessed_bit]
            else:
                judged += self.magie.incorrect_bits[guessed_bit]

        return judged


class ConsoleDecodingGuesser(ConsoleGuesser):
    def guess(self, current_correct=None) -> FullJudgment:
        self.magie.out(self.puzzle.win_bits)
        if not current_correct:
            current_correct = self.puzzle.init
        _input = input(current_correct)

        guess_text = current_correct + _input.upper()

        full_judgment: FullJudgment = self.puzzle.encoding.judge_text(guess_text, self.puzzle.win_text)

        encoded_correct_guess = self.puzzle.encoding.encode_bit_string(full_judgment.correct_guess)

        self.magie.out(encoded_correct_guess)

        return full_judgment

    def get_judgment_display(self, char_judgement: CharJudgment):
        """Return a string of bits, decorated according to their correctness, ready to display"""
        judged = ''

        for guessed_bit in self.puzzle.encoding.encode_bit_string(char_judgement.guess):
            if char_judgement.judgment in self.magie.on_bits:  # judgment indicates a correct bit
                judged += self.magie.correct_bits[guessed_bit]
            else:
                judged += self.magie.incorrect_bits[guessed_bit]

        return judged


def start_game(json_path):
    with open(json_path, encoding='utf-8') as menu_file:
        menu = Menu(file=menu_file)

    magie = ConsoleMAGiE()

    game = Game(menu, magie)
    game.run()


if __name__ == '__main__':
    start_game('TestMenus/FullMenu.json')
