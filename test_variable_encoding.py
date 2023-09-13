import unittest

from variable_width import VariableWidthEncoding

variable_encoding = {
    '1': {
        'A': '1',
        'B': '11',
        'C': '111',
        'D': '1111'
        },
    '0': {
        '': '0',
        ' ': '00',
        '.': '000'
    }
}


class TestVariableEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.encoding_under_test = VariableWidthEncoding(variable_encoding)

    def test_encode_D(self):
        self.assertEqual('1111', self.encoding_under_test.encode_bit_string('D'))

    def test_decode_111(self):
        self.assertEqual('C', self.encoding_under_test.decode('111'))

    def test_decode_char_separator(self):
        self.assertEqual('', self.encoding_under_test.decode('0'))

    def test_decode_00(self):
        self.assertEqual(' ', self.encoding_under_test.decode('00'))

    def test_encode_AB(self):
        self.assertEqual('1011', self.encoding_under_test.encode_bit_string('AB'))

    def test_encode_sentence(self):
        sentence = 'A CAB'
        expected_encoding = '10011101011'
        self.assertEqual(expected_encoding, self.encoding_under_test.encode_bit_string(sentence))

    def test_split_by_switch_1(self):
        encoded = '10011101011000'  # 'A CAB.'
        expected = ['1', '00', '111', '0', '1', '0', '11', '000']
        self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

    def test_split_by_switch_2(self):
        encoded = '101011101111'
        expected = ['1', '0', '1', '0', '111', '0', '1111']
        self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

    def test_split_all_same(self):
        encoded = '111111111111111111111111'  # 'X'
        expected = [encoded]
        self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

    def test_decode_sentence(self):
        sentence = '10011101011000'
        self.assertEqual('A CAB.', self.encoding_under_test.decode_bit_string(sentence))

    def test_judge_bits_by_character(self):
        guess = '101011101111'
        win = '1011011101111'
        expected_guess_split = ['1', '0', '0', '111', '0', '1111']
        expected_win_split = ['1', '0', '11', '0', '111', '0', '1111']
        expected = [(True, '1'), (True, '1'), (False, '0'), (True, '1'), (True, '111'), (False, '0'), (False, '0000')]
        all_correct, splits = self.encoding_under_test.judge_bits(guess, win)

        self.assertFalse(all_correct)
        self.assertEqual(7, len(splits))
        for i in range(len(expected)):
            self.assertEqual(expected[i][0], splits[i][0], f'split correct at {i}')
            self.assertEqual(expected[i][1], splits[i][1], f'split judgment at {i}')


if __name__ == '__main__':
    unittest.main()
