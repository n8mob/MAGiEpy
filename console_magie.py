from console_guessers import ConsoleFixedWidthEncodingGuesser, ConsoleEncodingGuesser, ConsoleDecodingGuesser, \
  ConsoleXorGuesser
from magie_display import MAGiEDisplay, Guesser
from magie_model import GuessMode, Menu, Category, Level, Puzzle

TITLE_LINE = '============='
THANK_YOU_FOR_PLAYOS = ['THANK YOU', 'FOR PLAYOS', 'MAGiE']

CORRECT = 'correct'
INCORRECT = 'incorrect'
RESET = 'reset'

ANSI_CODES = {
  CORRECT: '\u001B[36m',
  INCORRECT: '\u001B[31m',
  RESET: '\u001B[0m',
}


class ConsoleMAGiE(MAGiEDisplay):
  def __init__(self):
    super().__init__()
    self.on_bits = ['1']
    self.off_bits = ['0']
    self.ignore = [' ', ',', '_']

    self.decode_bits = ['0', '1', '?']

    Guesser.register_guesser('5bA1', 'Encode', ConsoleFixedWidthEncodingGuesser)
    Guesser.register_guesser('5bA1', 'Decode', ConsoleDecodingGuesser)
    Guesser.register_guesser('AlphaLengthA1', 'Encode', ConsoleEncodingGuesser)
    Guesser.register_guesser('AlphaLengthA1', 'Decode', ConsoleDecodingGuesser)
    Guesser.register_guesser('xorF', 'Encode', ConsoleXorGuesser)
    Guesser.register_guesser('xorF', 'Decode', ConsoleXorGuesser)

  def preferred_guess_mode(self) -> GuessMode:
    return GuessMode.MULTI_BIT

  def out(self, text):
    if isinstance(text, str):
      prepared = self.prep(text)
      print(prepared)
    else:
      for line in text:
        prepared = self.prep(line)
        print(prepared)

  def read(self, prompt='', include_prompt=False):
    prompt = self.prep(prompt)
    _input = self.prep(input(prompt))
    if include_prompt:
      return prompt + _input
    else:
      return _input

  def prep(self, text):
    u = ''.join((c.lower() if c in ['i', 'I'] else c.upper() for c in text))
    for code in ANSI_CODES:
      u = u.replace(ANSI_CODES[code].upper(), ANSI_CODES[code])
    return u

  def prep_correct(self, guessed_bit):
    return ANSI_CODES[CORRECT] + guessed_bit

  def prep_incorrect(self, guessed_bit):
    return ANSI_CODES[INCORRECT] + guessed_bit

  def is_on(self, bit):
    return bit in self.on_bits

  def is_off(self, bit):
    return bit in self.off_bits

  def prep_judgement(self, char_judgement):
    return super().prep_judgement(char_judgement) + ANSI_CODES[RESET]

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

    while not judgment.is_correct:
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
