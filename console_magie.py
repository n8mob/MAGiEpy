from magie_display import MAGiEDisplay, Guesser
from magie_model import GuessMode, Menu, Category, Level, Puzzle

TITLE_LINE = '============='
THANK_YOU_FOR_PLAYOS = ['THANK YOU', 'FOR PLAYOS', 'MAGiE']


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

  def out(self, text):
    if isinstance(text, str):
      print(self.prep(text))
    else:
      for line in text:
        print(self.prep(line))

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
    self.out([
      'welcome to MAGiE',
      TITLE_LINE,
      ''
    ])

  def show_error(self, error):
    if isinstance(error, str):
      error = [error]
    self.out([TITLE_LINE] + error + [TITLE_LINE])

  def select_category(self, menu: Menu):
    for i, category in enumerate(menu.categories):
      self.out(f'{i:>2} {category.name}')

    category_number = -1

    while category_number < 0:
      try:
        category_number = int(input('select category: '))
      except ValueError:
        print(f'Please choose a number: 0-{len(menu.categories)}')
        category_number = -1

    return menu.categories[category_number]

  def select_level(self, category: Category, menu_commands):
    for i, level in enumerate(category.levels):
      pre = f'{i:>2}'
      for line in level.levelName:
        self.out(f'{pre} {line}')
        pre = ' ' * len(pre)

    if menu_commands:
      self.out('  or')
      for command_input, menu_command in menu_commands.items():
        self.out(f'{command_input} {menu_command}')

    selected = input('select level: ').upper()
    if selected in menu_commands:
      return selected

    level_number = int(selected)

    return category.levels[level_number]

  def start_level(self, level: Level):
    level.current_puzzle_index = 0

  def finish_level(self, level: Level):
    self.out(['GOOD WORK!', 'YOU FINISHOS', 'THE LEVEL']
             + level.levelName
             + [TITLE_LINE, '']
             )

  def start_puzzle(self, puzzle: Puzzle):
    for line in puzzle.clue:
      self.out(line)

    guesser = Guesser.for_puzzle(self, puzzle)
    judgment = guesser.guess()

    while not judgment.correct:
      judgment = guesser.guess(judgment.correct_guess)

    self.win_puzzle(puzzle)

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

  def quit(self, quit_message=None):
    if not quit_message:
      quit_message = THANK_YOU_FOR_PLAYOS
    elif isinstance(quit_message, str):
      quit_message = [quit_message]

    self.out('')
    self.out(TITLE_LINE)
    for line in quit_message:
      self.out(line)
