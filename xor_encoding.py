import math

from binary_encoding import BinaryEncoding

XOR_ENCODING = 'xor_encoding'


class XorEncoding(BinaryEncoding):
  def __init__(self, key):
    super().__init__(XOR_ENCODING)
    self.key = key
    self.key_length = len(f'{key:X}')

  def xor(self, c, base=16):
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
      xor = chunk_i ^ self.key
      output += f'{xor:X}'
    return int(output, 16)

  def encode(self, c):
    return self.xor(c)

  def decode(self, c):
    return self.xor(c)

  def xor_string(self, bit_string):
    b = ''
    for c in bit_string:
      i = int(c, 16)
      b += f'{self.encode(i):X}'
    return b

  def encode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)

  def decode_bit_string(self, bit_string) -> str:
    return self.xor_string(bit_string)
