import unittest

from Encodings import FixedWidthEncoding

A1 = {
    'A': 1,
    'B': 2,
    '_': 0
}


class TestFixedEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.encoding_under_test = FixedWidthEncoding(5, A1)

    def test_reversed_dictionary(self):
        self.assertIsNotNone(self.encoding_under_test.decoding)

        self.assertFalse({})
        self.assertTrue(self.encoding_under_test.decoding)
        self.assertIn(0, self.encoding_under_test.decoding)
        self.assertEqual('A', self.encoding_under_test.decoding[1])

    def test_make_bit_string_A(self):
        self.assertEqual('00001', self.encoding_under_test.encode_bit_string('A'))

    def test_make_bit_string_B(self):
        self.assertEqual('00010', self.encoding_under_test.encode_bit_string('B'))

    def test_encode_A(self):
        self.assertEqual(1, self.encoding_under_test.encode('A'))

    def test_encode_B(self):
        self.assertEqual(2, self.encoding_under_test.encode('B'))

    def test_encode_space(self):
        self.assertEqual(0, self.encoding_under_test.encode('_'))

    def test_decode_1(self):
        self.assertEqual('A', self.encoding_under_test.decode(1))

    def test_decode_2(self):
        self.assertEqual('B', self.encoding_under_test.decode(2))

    def test_decode_Zero(self):
        self.assertEqual('_', self.encoding_under_test.decode(0))

    def test_encode_B_width_8(self):
        self.encoding_under_test = FixedWidthEncoding(8, A1)
        self.assertEqual('00000010', self.encoding_under_test.encode_bit_string('B'))

    def test_decode_bit_string_1(self):
        self.assertEqual('A', self.encoding_under_test.decode_bit_string('1'))

    def test_decode_bit_string_10(self):
        self.assertEqual('B', self.encoding_under_test.decode_bit_string('10'))

    def test_decode_bit_string_0(self):
        self.assertEqual('_', self.encoding_under_test.decode_bit_string('0'))


if __name__ == '__main__':
    unittest.main()
