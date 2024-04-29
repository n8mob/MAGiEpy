from judgments import FullJudgment


class BinaryEncoding:
  def __init__(self, encoding_type):
    self.encoding_type = encoding_type

  def decode(self, enc):
    pass

  def encode(self, c):
    pass

  def decode_bit_string(self, bit_string):
    pass

  def encode_bit_string(self, c) -> str:
    """
    given a character, encode it and return the bits as a string of 1's and 0's
    Args:
        c: character to decode

    Returns: a string of 1's and 0's representing the binary encoding of the given character

    """
    pass

  def judge_bits(self, guess_bits, win_bits) -> FullJudgment:
    pass

  def judge_text(self, guess_text, win_text) -> FullJudgment:
    pass
