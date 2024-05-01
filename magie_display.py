from abc import ABC, abstractmethod

from judgments import FullJudgment
from magie_model import Menu, Category, Puzzle, Level, GuessMode


class MAGiEDisplay(ABC):
  def __init__(self):
    self.puzzle = None

  @abstractmethod
  def preferred_guess_mode(self) -> GuessMode:
    pass

  @abstractmethod
  def boot_up(self):
    pass

  @abstractmethod
  def select_category(self, menu: Menu) -> Category:
    pass

  @abstractmethod
  def select_level(self, category: Category, menu_commands) -> Level:
    pass

  @abstractmethod
  def start_level(self, level: Level):
    pass

  @abstractmethod
  def finish_level(self, level: Level):
    pass

  @abstractmethod
  def start_puzzle(self, puzzle: Puzzle):
    pass

  @abstractmethod
  def win_puzzle(self, puzzle: Puzzle):
    pass

  @abstractmethod
  def guess_1_char(self):
    pass

  @abstractmethod
  def guess_text(self, init, win_text):
    pass

  @abstractmethod
  def show_error(self, error):
    pass

  @abstractmethod
  def reset(self):
    pass

  @abstractmethod
  def quit(self):
    pass

  @abstractmethod
  def prep(self, text):
    raise NotImplementedError

  def prep_judgement(self, char_judgement):
    judged = ''

    for i, bit_judgment in enumerate(char_judgement.bit_judgments):
      if i < len(char_judgement.guess_bits):
        guessed_bit = char_judgement.guess_bits[i]
      else:
        guessed_bit = '0'

      if self.is_on(bit_judgment):  # bit_judgments indicates a correct bit
        judged += self.prep_correct(guessed_bit)
      else:
        judged += self.prep_incorrect(guessed_bit)

    return judged

  @abstractmethod
  def prep_correct(self, guessed_bit):
    pass

  @abstractmethod
  def prep_incorrect(self, guessed_bit):
    pass

  @abstractmethod
  def is_on(self, bit) -> bool:
    pass

  def is_off(self, bit) -> bool:
    return not self.is_on(bit)

  @abstractmethod
  def out(self, text):
    raise NotImplementedError


class Guesser(ABC):
  registered_guessers = {}

  @classmethod
  def register_guesser(cls, encoding, puzzle_type, guesser):
    cls.registered_guessers[(encoding, puzzle_type)] = guesser

  def __init__(self, magie: MAGiEDisplay, puzzle: Puzzle):
    self.magie: MAGiEDisplay = magie
    self.puzzle: Puzzle = puzzle

  @classmethod
  def for_puzzle(cls, magie, puzzle: Puzzle):
    return cls.registered_guessers[(puzzle.encoding_id, puzzle.type)](magie, puzzle)

  @abstractmethod
  def guess(self, current_guess=None) -> FullJudgment:
    pass
