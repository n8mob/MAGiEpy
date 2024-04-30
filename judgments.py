class CharJudgment:
  correct: bool
  guess: str
  judgment: str

  def __init__(self, correct, guess, judgment):
    self.correct = correct
    self.guess = guess
    self.judgment = judgment

  def __repr__(self):
    return f"({self.correct}, '{self.guess}', '{self.judgment})"

  def __eq__(self, o) -> bool:
    if isinstance(o, CharJudgment):
      return ((self.correct == o.correct)
              and (self.guess == o.guess)
              and (self.judgment == o.judgment))
    elif hasattr(o, '__getitem__'):
      return ((self.correct == o[0])
              and (self.guess == o[1])
              and (self.judgment == o[2]))

  def __hash__(self) -> int:
    return hash(self.correct) + hash(self.guess) + hash(self.judgment)


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
