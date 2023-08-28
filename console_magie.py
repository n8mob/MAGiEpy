from MagieModel import Menu, Category, Puzzle, Level
from Game import Game
from magie_display import MAGiEDisplay, TITLE_LINE


class ConsoleMAGiE(MAGiEDisplay):
    @staticmethod
    def out(text=''):
        print(ConsoleMAGiE.prep(text))

    @staticmethod
    def prep(text):
        u = ''.join((c.lower() if c in ['i', 'I'] else c.upper() for c in text))
        return u

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
        for line in puzzle.winMessage:
            self.out(line)

    def guess_bit(self):
        return input()

    def guess_char(self):
        return input()

    def guess_text(self, init, win_text):
        guess_text = input(init)
        max_check = min(len(guess_text), len(win_text))
        correct_guesses = ''
        for i in range(max_check):
            if guess_text[i] == win_text[i]:
                correct_guesses += win_text[i]
            else:
                correct_guesses += ' '
        self.out(correct_guesses)
        return correct_guesses.rstrip()

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
