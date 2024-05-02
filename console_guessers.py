from abc import ABC

import console_magie
from fixed_width import FixedWidthEncoding
from judgments import FullJudgment
from magie_display import Guesser
from magie_model import Puzzle


class ConsoleGuesser(Guesser, ABC):
  def __init__(self, magie, puzzle):
    super().__init__(magie, puzzle)

  def prompt(self, current_correct) -> str:
    return (current_correct or '') + input(current_correct or '')


class ConsoleEncodingGuesser(ConsoleGuesser):
  def __init__(self, magie, puzzle):
    super().__init__(magie, puzzle)

  def guess(self, current_guess=None) -> FullJudgment:
    if not current_guess:
      current_guess = self.puzzle.encoding.encode_bit_string(self.puzzle.init)

    _input = self.prompt(current_guess)

    guess_bits = ''

    for b in _input:
      if self.magie.is_on(b):
        guess_bits += '1'
      elif self.magie.is_off(b):
        guess_bits += '0'
      else:
        continue  # skip invalid bits
        # we could skip self.ignore and throw on others, if we want

    full_judgment: FullJudgment = self.puzzle.encoding.judge_bits(current_guess + guess_bits, self.puzzle.win_bits)

    for i, char_judgment in enumerate(full_judgment.char_judgments):
      judged_bits_display = self.magie.prep_judgement(char_judgment)

      decoded_guess = self.puzzle.encoding.decode_bit_string(char_judgment.guess_bits)
      display = f'{decoded_guess} {judged_bits_display}'
      self.magie.out(display)

    return full_judgment

  def split_characters(self, bitstring):
    return


class ConsoleDecodingGuesser(ConsoleGuesser):
  def guess(self, current_guess=None) -> FullJudgment:
    self.magie.out(self.puzzle.win_bits)
    if not current_guess:
      current_guess = self.puzzle.init
    _input = input(current_guess)

    guess_text = current_guess + self.magie.prep(_input)
    win_text = self.magie.prep(self.puzzle.win_text)

    full_judgment: FullJudgment = self.puzzle.encoding.judge_text(guess_text, win_text)

    encoded_correct_guess = self.puzzle.encoding.encode_bit_string(full_judgment.correct_guess)

    self.magie.out(encoded_correct_guess)

    return full_judgment


class ConsoleFixedWidthEncodingGuesser(ConsoleEncodingGuesser):
  def __init__(self, magie, puzzle):
    super().__init__(magie, puzzle)
    if isinstance(puzzle.encoding, FixedWidthEncoding):
      self.encoding: FixedWidthEncoding = puzzle.encoding
    else:
      raise TypeError(f'Expecting a fixed-width encoding, not {puzzle.encoding.encoding_type}')

  def prompt(self, current_correct):
    for char_bits in self.split_characters(current_correct):
      self.magie.out(self.encoding.decode_bit_string(char_bits) + ' ' + char_bits)
    return input()

  def split_characters(self, bitstring):
    return self.encoding.split_bitstring(bitstring)


class ConsoleXorGuesser(ConsoleGuesser):
  """A special-case guesser: encode and decode are the same."""
  def __init__(self, magie, puzzle: Puzzle):
    super().__init__(magie, puzzle)

  def guess(self, current_guess=None) -> FullJudgment:
    if not self.puzzle.win_bits:  # No win_bits to compare, so defaults to correct
      return FullJudgment(is_correct=True, correct_guess='', char_judgments=[])

    current_guess = self.prompt(current_guess)

    xored_guess = self.puzzle.encoding.encode_bit_string(current_guess)
    if not xored_guess:
      return FullJudgment(is_correct=False, correct_guess='')

    xor_is_correct = xored_guess == self.puzzle.win_bits
    if xor_is_correct:
      correct_guess = current_guess
    else:
      correct_guess = ''
    return FullJudgment(is_correct=xor_is_correct, correct_guess=correct_guess)


