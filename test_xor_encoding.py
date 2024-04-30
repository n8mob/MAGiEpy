from unittest import TestCase

from xor_encoding import XorEncoding


class TestXorEncoding(TestCase):
  def setUp(self):
    self.xorF = XorEncoding(key='F')
    self.xor0 = XorEncoding(key='0')
    self.xor0000 = XorEncoding(key='0000')

  def test_0_and_0(self):
    expected = 0x0
    actual = self.xor0.encode(0x0)
    self.assertEqual(expected, actual)

  def test_F_and_F(self):
    expected = 0x0
    actual = self.xorF.encode(0xF)
    self.assertEqual(expected, actual)

  def test_encode_D_with_key_0(self):
    d = 0b1101
    expected = 0b1101
    actual = self.xor0.encode(d)
    self.assertEqual(expected, actual)

  def test_encode_D_with_key_F(self):
    d = 0b1101
    expected = 0b0010
    actual = self.xorF.encode(d)
    self.assertEqual(expected, actual)

  def test_encode_ABCD_with_key_0000(self):
    abcd = 0xABCD
    expected = 0xABCD
    actual = self.xor0000.encode(abcd)
    self.assertEqual(expected, actual)

  def test_encode_ABCD_with_key_1234(self):
    """ 0xABCD ^ 0x1234 = 0xB9F9
    0x1234 = 0001 0010 0011 0100
    0xABCD = 1010 1011 1100 1101
    0xB9F9 = 1011 1001 1111 1001
    """
    unit = XorEncoding(key_int=0x1234)
    abcd = 0xABCD
    expected = 0xB9F9
    actual = unit.encode(abcd)
    self.assertEqual(expected, actual)

  def test_encode_string_with_key_0(self):
    abcd = 'ABCD'
    expected = 'ABCD'
    actual = self.xor0.encode_bit_string(abcd)
    self.assertEqual(expected, actual)

  def test_decode_string_with_key_F(self):
    """ 123ABC ^ 0 = ?
    0x123ABC = 0001 0010 0011 1010 1011 1100
    0xF      = 1111 ...
    0xEDC543 = 1110 1101 1100 0101 0100 0011
    :return:
    """
    s = '123ABC'
    expected = 'EDC543'
    actual = self.xorF.decode_bit_string(s)
    self.assertEqual(expected, actual)

  def test_encode_longer_than_key_0(self):
    abcd = 'ABCD'
    expected = 0xABCD
    actual = self.xor0.encode(abcd)
    self.assertEqual(expected, actual)

  def test_encode_longer_than_key_F(self):
    """ 0xABCD ^ 0xF = ?
    0xABCD = 1010 1011 1100 1101
    0xF    = 1111 ...
    0x5432 = 0101 0100 0011 0010
    """
    abcd = 'ABCD'
    expected = 0x5432
    actual = self.xorF.encode(abcd)
    self.assertEqual(expected, actual, f'{abcd} ^ {self.xorF.key:X} = {actual:X}, expected {expected:X}')
