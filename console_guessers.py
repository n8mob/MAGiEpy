from console_magie import ConsoleMAGiE
from fixed_width import FixedWidthEncoding
from judgments import FullJudgment, CharJudgment
from magie_display import Guesser
from magie_model import Puzzle, MissingEncodingError


class ConsoleGuesser(Guesser):
  registered_guessers = {}

  def __init__(self, magie: ConsoleMAGiE, puzzle):
    super().__init__(magie, puzzle)
    self.magie: ConsoleMAGiE = magie

  def prompt(self, current_correct) -> str:
    return input(current_correct)

  @classmethod
  def register_guesser(cls, encoding, guesser: Guesser):
    cls.registered_guessers[encoding] = guesser

  @classmethod
  def for_puzzle(cls, magie, puzzle: Puzzle):
    if puzzle.type == 'Decode':
      return ConsoleDecodingGuesser(magie, puzzle)
    elif puzzle.type == 'Encode':
      return ConsoleEncodingGuesser(magie, puzzle)
    elif puzzle.type == 'Other':
      return ConsoleXorGuesser(magie, puzzle)
    else:
      raise MissingEncodingError(puzzle.type)


class ConsoleEncodingGuesser(ConsoleGuesser):
  def __init__(self, magie, puzzle):
    super().__init__(magie, puzzle)
    super().register_guesser(puzzle.encoding_id, self)

  def guess(self, current_correct=None) -> FullJudgment:
    if not current_correct:
      current_correct = self.puzzle.encoding.encode_bit_string(self.puzzle.init)

    _input = self.prompt(current_correct)

    guess_bits = ''

    for b in _input:
      if b in self.magie.on_bits:
        guess_bits += '1'
      elif b in self.magie.off_bits:
        guess_bits += '0'
      else:
        continue  # skip invalid bits
        # we could skip self.ignore and throw on others, if we want

    full_judgment: FullJudgment = self.puzzle.encoding.judge_bits(current_correct + guess_bits, self.puzzle.win_bits)

    for i, char_judgment in enumerate(full_judgment.char_judgments):
      judged_bits_display = self.get_judgment_display(char_judgment)

      decoded_guess = self.puzzle.encoding.decode_bit_string(char_judgment.guess_bits)
      self.magie.out(decoded_guess + ' ' + char_judgment.guess_bits + ' ' + judged_bits_display)

    return full_judgment

  def get_judgment_display(self, char_judgement: CharJudgment):
    """Return a string of bits, decorated according to their correctness, ready to display"""
    judged = ''

    for i, bit_judgment in enumerate(char_judgement.bit_judgments):
      if i < len(char_judgement.guess_bits):
        guessed_bit = char_judgement.bit_judgments[i]
      else:
        guessed_bit = '0'

      if bit_judgment in self.magie.on_bits:  # bit_judgments indicates a correct bit
        judged += self.magie.correct_bits[guessed_bit]
      else:
        judged += self.magie.incorrect_bits[guessed_bit]

    return judged

  def split_characters(self, bitstring):
    return


class ConsoleDecodingGuesser(ConsoleGuesser):
  def guess(self, current_correct=None) -> FullJudgment:
    self.magie.out(self.puzzle.win_bits)
    if not current_correct:
      current_correct = self.puzzle.init
    _input = input(current_correct)

    guess_text = current_correct + self.magie.prep(_input)
    win_text = self.magie.prep(self.puzzle.win_text)

    full_judgment: FullJudgment = self.puzzle.encoding.judge_text(guess_text, win_text)

    encoded_correct_guess = self.puzzle.encoding.encode_bit_string(full_judgment.correct_guess)

    self.magie.out(encoded_correct_guess)

    return full_judgment

  def get_judgment_display(self, char_judgement: CharJudgment):
    """Return a string of bits, decorated according to their correctness, ready to display"""
    judged = ''

    for guessed_bit in self.puzzle.encoding.encode_bit_string(char_judgement.guess_bits):
      if char_judgement.bit_judgments in self.magie.on_bits:  # bit_judgments indicates a correct bit
        judged += self.magie.correct_bits[guessed_bit]
      else:
        judged += self.magie.incorrect_bits[guessed_bit]

    return judged


class ConsoleFixedWidthEncodingGuesser(ConsoleEncodingGuesser):
  def __init__(self, magie: ConsoleMAGiE, puzzle):
    super().__init__(magie, puzzle)
    if isinstance(puzzle.encoding, FixedWidthEncoding):
      self.encoding: FixedWidthEncoding = puzzle.encoding
    else:
      raise TypeError(f'Expecting a fixed-width encoding, not {puzzle.encoding.encoding_type}')

  def prompt(self, current_correct):
    for char_bits in self.split_characters(current_correct):
      self.magie.out(self.encoding.decode_bit_string(char_bits) + ' ' + char_bits)

  def split_characters(self, bitstring):
    return self.encoding.split_bitstring(bitstring)


class ConsoleXorGuesser(ConsoleGuesser):
  def __init__(self, magie: ConsoleMAGiE, puzzle: Puzzle):
    super().__init__(magie, puzzle)

  def guess(self, current_correct=None) -> FullJudgment:
    xor_result = self.puzzle.win_bits ^ current_correct
    return FullJudgment(correct=None, correct_guess=None, char_judgments=xor_result)
