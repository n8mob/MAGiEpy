class CharJudgment:
  """
  is_char_correct: is the guessed character (the letter encoded by the guess bits) correct
  guess: a bit-string representing the player's guess
  judgement: a bitstring representing the correctness of each symbol (bit) in the guess
  """
  is_char_correct: bool
  guess_bits: str
  judgment: str

  def __init__(self, correct, guess, judgment):
    """
    :param correct:
    :param guess:
    :param judgment:
    """
    self.is_char_correct = correct
    self.guess_bits = guess
    self.judgment = judgment

  def __repr__(self):
    return f"({self.is_char_correct}, '{self.guess_bits}', '{self.judgment})"

  def __eq__(self, o) -> bool:
    if isinstance(o, CharJudgment):
      return ((self.is_char_correct == o.is_char_correct)
              and (self.guess_bits == o.guess_bits)
              and (self.judgment == o.judgment))
    elif hasattr(o, '__getitem__'):
      return ((self.is_char_correct == o[0])
              and (self.guess_bits == o[1])
              and (self.judgment == o[2]))

  def __hash__(self) -> int:
    return hash(self.is_char_correct) + hash(self.guess_bits) + hash(self.judgment)


class FullJudgment:
  char_judgments: [CharJudgment]

  def __init__(self, correct, correct_guess, char_judgments):
    self.correct = correct
    self.correct_guess = correct_guess
    self.char_judgments: [CharJudgment] = []

    if char_judgments:
      for char_judgment in char_judgments:
        if isinstance(char_judgment, CharJudgment):
          self.char_judgments.append(char_judgment)
        elif isinstance(char_judgment, tuple):
          self.char_judgments.append(CharJudgment(*char_judgment))

  def __iter__(self):
    return iter((self.correct, self.correct_guess, self.char_judgments))
