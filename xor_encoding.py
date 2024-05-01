import math

from binary_encoding import BinaryEncoding

XOR_ENCODING = 'xor_encoding'


class XorEncoding(BinaryEncoding):
  def __init__(self, key=None, base=16, **kwargs):
    """
    :param key: key as string encoded in the given base (default to base 16)
    :param base: defaults to 16-bit (hexadecimal)
    :param kwargs: key_int is the integer key (thus bypassing the parsing and base arguments)
    """
    super().__init__(XOR_ENCODING)
    if not key:
      self.key = kwargs['key_int']
    else:
      self.key = int(key, base)
    self.key_length = len(f'{self.key:X}')

  def xor_with_key(self, c, base=16):
    if isinstance(c, str):
      i = int(c, base)
    else:
      i = int(c)

    c_hex = f'{i:X}'
    c_length = len(c_hex)
    chunks = math.ceil(c_length / self.key_length)

    output = ''

    for chunk_index in range(chunks):
      chunk = c_hex[chunk_index:chunk_index + self.key_length]
      chunk_i = int(chunk, base)
      xor = chunk_i ^ self.key  # ah! x-oring as part of "encoding"... is that the right thing? maybe not.
      output += f'{xor:X}'
    return int(output, 16)

  def encode(self, c):
    return self.xor_with_key(c)

  def decode(self, c):
    return self.xor_with_key(c)

  def xor_string(self, bit_string):  # not really a "bit" string, is it...
    b = ''
    for c in bit_string:
      i = int(c, 16)
      b += f'{self.encode(i):X}'
    return b

  def encode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)

  def decode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)
