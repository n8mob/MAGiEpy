class CharJudgment:
  is_char_correct: bool
  guess_bits: str
  bit_judgments: str

  def __init__(self, is_char_correct, guess_bits, bit_judgements):
    """
    :param is_char_correct: is the guessed character (the letter encoded by guess_bits) correct
    :param guess_bits: a bit-string representing the player's guess
    :param bit_judgements: a bitstring representing the correctness of each symbol (bit) in the guess
    """
    self.is_char_correct = is_char_correct
    self.guess_bits = guess_bits
    self.bit_judgments = bit_judgements

  def __repr__(self):
    return f"({self.is_char_correct}, '{self.guess_bits}', '{self.bit_judgments}')"

  def __eq__(self, o) -> bool:
    if isinstance(o, CharJudgment):
      return ((self.is_char_correct == o.is_char_correct)
              and (self.guess_bits == o.guess_bits)
              and (self.bit_judgments == o.bit_judgments))
    elif hasattr(o, '__getitem__'):
      return ((self.is_char_correct == o[0])
              and (self.guess_bits == o[1])
              and (self.bit_judgments == o[2]))

  def __hash__(self) -> int:
    return hash(self.is_char_correct) + hash(self.guess_bits) + hash(self.bit_judgments)


class FullJudgment:
  """A judgment for the entire puzzle.

  related: CharJudgment holds a judgment for a single character."""
  char_judgments: [CharJudgment]

  def __init__(self, is_correct, correct_guess, char_judgments=None):
    """
    :param is_correct: True if the entire puzzle is correct.
    :param correct_guess: those parts (bits) of the guess that are correct
    Usually only up to the first incorrect bit or character.
    :param char_judgments: list of CharJudgments for each character in the guess
    """
    self.is_correct = is_correct
    self.correct_guess = correct_guess
    self.char_judgments: [CharJudgment] = []

    if char_judgments:
      for char_judgment in char_judgments:
        if isinstance(char_judgment, CharJudgment):
          self.char_judgments.append(char_judgment)
        elif isinstance(char_judgment, tuple):
          self.char_judgments.append(CharJudgment(*char_judgment))
    else:
      char_judgments = []

  def __iter__(self):
    return iter((self.is_correct, self.correct_guess, self.char_judgments))
