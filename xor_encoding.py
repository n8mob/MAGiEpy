import math

from binary_encoding import BinaryEncoding
from judgments import FullJudgment, CharJudgment

XOR_ENCODING = 'xor_encoding'


class XorEncoding(BinaryEncoding):
  def __init__(self, key=None, base=16, **kwargs):
    """
    :param key: key as string encoded in the given base (default to base 16)
    :param base: defaults to 16-bit (hexadecimal)
    :param kwargs: key_int is the integer key (thus bypassing the parsing and base arguments)
    """
    super().__init__(XOR_ENCODING)
    self.base = base
    if not key:
      self.key = kwargs['key_int']
    else:
      self.key = int(key, base)
    self.key_length = len(f'{self.key:X}')

  def xor_with_key(self, c, base=None):
    xored_chunks = []

    if not c:
      return xored_chunks

    if base is None:
      base = self.base

    i = int(c, base)

    c_hex = f'{i:X}'
    c_length = len(c_hex)
    chunks = math.ceil(c_length / self.key_length)

    for chunk_index in range(chunks):
      chunk = c_hex[chunk_index:chunk_index + self.key_length]
      chunk_i = int(chunk, base)
      xored_chunks.append(chunk_i ^ self.key)  # ah! x-oring => "encoding"... is that the right thing? maybe not.

    return xored_chunks

  def xor_to_text(self, c, base=None):
    xored_chunks = self.xor_with_key(c, base)
    output = ''.join(f'{xor:X}' for xor in xored_chunks)
    return int(output, self.base)

  def encode(self, c):
    return self.xor_to_text(c)

  def decode(self, c):
    return self.xor_to_text(c)

  def xor_string(self, bit_string):  # not really a "bit" string, is it...
    b = ''

    if bit_string:
      for c in bit_string:
        b += f'{self.encode(c):X}'
    return b

  def encode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)

  def decode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)

  def judge_guess(self, guess, win):
    xored_chunks = self.xor_with_key(guess)
    common_length = min(len(xored_chunks), len(win))
    char_judgments = []
    is_correct = True
    correct_guess = ''
    for i in range(common_length):
      is_char_correct = xored_chunks[i] == win[i]
      is_correct = is_correct and is_char_correct
      if is_char_correct:
        correct_guess += guess[i]
      char_judgments.append(CharJudgment(is_char_correct, guess_bits=guess[i], bit_judgements=xored_chunks[i]))

    return FullJudgment(is_correct, correct_guess, char_judgments)

  def judge_bits(self, guess_bits, win_bits):
    return self.judge_guess(guess_bits, win_bits)

  def judge_text(self, guess_text, win_text) -> FullJudgment:
    return self.judge_guess(guess_text, win_text)
