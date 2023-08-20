import unittest

from Encodings import FixedWidthEncoding

hexadecimal = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15
}


class TestFixedEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.encoding_under_test = FixedWidthEncoding(4, hexadecimal)

    def test_reversed_dictionary(self):
        self.assertIsNotNone(self.encoding_under_test.decoding)

        self.assertFalse({})
        self.assertTrue(self.encoding_under_test.decoding)
        self.assertIn(0, self.encoding_under_test.decoding)
        self.assertEqual('1', self.encoding_under_test.decoding[1])

    def test_make_bit_string_A(self):
        self.assertEqual('1010', self.encoding_under_test.encode_bit_string('A'))

    def test_make_bit_string_B(self):
        self.assertEqual('1011', self.encoding_under_test.encode_bit_string('B'))

    def test_encode_A(self):
        self.assertEqual(1, self.encoding_under_test.encode('1'))

    def test_encode_B(self):
        self.assertEqual(2, self.encoding_under_test.encode('2'))

    def test_encode_space(self):
        self.assertEqual(0, self.encoding_under_test.encode('0'))

    def test_decode_1(self):
        self.assertEqual('1', self.encoding_under_test.decode(1))

    def test_decode_2(self):
        self.assertEqual('2', self.encoding_under_test.decode(2))

    def test_decode_Zero(self):
        self.assertEqual('0', self.encoding_under_test.decode(0))

    def test_encode_B_width_8(self):
        self.encoding_under_test = FixedWidthEncoding(8, hexadecimal)
        self.assertEqual('00000010', self.encoding_under_test.encode_bit_string('2'))

    def test_decode_bit_string_1(self):
        self.assertEqual('1', self.encoding_under_test.decode_bit_string('1'))

    def test_decode_bit_string_10(self):
        self.assertEqual('2', self.encoding_under_test.decode_bit_string('10'))

    def test_decode_bit_string_0(self):
        self.assertEqual('0', self.encoding_under_test.decode_bit_string('0'))

    def test_decode_too_long_bitstring_0s(self):
        self.assertEqual('F', self.encoding_under_test.decode_bit_string('00001111'))

    def test_decode_too_long_bitstring_1s(self):
        self.assertEqual('7', self.encoding_under_test.decode_bit_string('111'))


if __name__ == '__main__':
    unittest.main()
