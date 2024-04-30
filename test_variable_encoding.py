import unittest

from judgments import FullJudgment
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

  def test_split_by_switch_with_punk_at_end(self):
    encoded = '10011101011000'  # 'A CAB.'
    expected = ['1', '00', '111', '1', '11', '000']
    self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

  def test_split_by_switch_with_letter_at_end(self):
    encoded = '101011101111'
    expected = ['1', '1', '111', '1111']
    self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

  def test_split_all_same(self):
    encoded = '111111111111111111111111'  # 'X'
    expected = [encoded]
    self.assertEqual(expected, self.encoding_under_test.split_by_switch(encoded))

  def test_decode_sentence(self):
    sentence = '10011101011000'
    self.assertEqual('A CAB.', self.encoding_under_test.decode_bit_string(sentence))

  def test_judge_single_correct_character(self):
    guess = '1111'
    win = '1111'
    expected_char_judgment = (True, '1111', '1111')
    actual = self.encoding_under_test.judge_bits(guess, win)

    self.assertTrue(actual.correct)
    self.assertEqual(guess, actual.correct_guess)
    self.assertEqual(1, len(actual.char_judgments))
    self.assertEqual(expected_char_judgment, actual.char_judgments[0])

  def test_judge_single_incorrect(self):
    guess = '111'
    win = '1111'

    actual = self.encoding_under_test.judge_bits(guess, win).char_judgments[0]

    self.assertFalse(actual.is_char_correct)
    self.assertEqual(guess, actual.guess_bits)
    self.assertEqual('1110', actual.bit_judgments)

  def test_judge_bits_by_character(self):
    guess = '101011101111'
    win = '1011011101111'
    expected = FullJudgment(False, '', [(True, '1', '1'),
      (False, '1', '10'),
      (True, '111', '111'),
      (True, '1111', '1111')])
    actual = self.encoding_under_test.judge_bits(guess, win)

    self.assertFalse(actual.correct)
    self.assertEqual(4, len(actual.char_judgments))
    for i in range(len(expected.char_judgments)):
      self.assertEqual(
        expected.char_judgments[i].is_char_correct, actual.char_judgments[i].is_char_correct, f'char correct at {i}')
      self.assertEqual(
        expected.char_judgments[i].guess_bits, actual.char_judgments[i].guess_bits, f'guess char at {i}')
      self.assertEqual(
        expected.char_judgments[i].bit_judgments, actual.char_judgments[i].bit_judgments, f'char judgment at {i}')

  def test_partial_correct_guess_char_is_returned(self):
    guess = '1010101'
    win = '10110101'

    all_correct, correct_guess_chars, _ = self.encoding_under_test.judge_bits(guess, win)
    self.assertFalse(all_correct)
    self.assertEqual('101', correct_guess_chars)

  def test_partial_correct_guess_chars_returned(self):
    guess = '1010101'
    win = '10101011'

    all_correct, correct_guess_chars, _ = self.encoding_under_test.judge_bits(guess, win)
    self.assertFalse(all_correct)
    self.assertEqual('1010101', correct_guess_chars)

  def test_correct_guess_punctuation_join(self):
    guess = '100110111'
    win = '100110111000'  # 'A BC.'
    expected_correct_guess_chars = '100110111'
    full_judgment = self.encoding_under_test.judge_bits(guess, win)
    all_correct = full_judgment.correct
    actual_correct_guess = full_judgment.correct_guess
    self.assertFalse(all_correct)
    self.assertEqual(expected_correct_guess_chars, actual_correct_guess)

  def test_only_period(self):
    guess = '000'
    win = '000'

    expected_char_judgment = (True, '000', '111')

    full_judgment = self.encoding_under_test.judge_bits(guess, win)

    self.assertTrue(full_judgment.correct)
    self.assertEqual(full_judgment.correct_guess, guess)
    actual_char_judgment = full_judgment.char_judgments[0]
    self.assertEqual(expected_char_judgment, actual_char_judgment)

  def test_ones_guess_too_short(self):
    guess = '1'
    win = '111'

    expected_char_judgment = '10'

    actual = self.encoding_under_test.judge_bits(guess, win).char_judgments[0]
    self.assertEqual(expected_char_judgment, actual.bit_judgments)

  def test_ones_guess_too_long(self):
    guess = '111'
    win = '1'

    expected_char_judgment = '10'
    actual = self.encoding_under_test.judge_bits(guess, win).char_judgments[0]

    self.assertEqual(expected_char_judgment, actual.bit_judgments)

  def test_zeros_guess_too_short(self):
    guess = '00'
    win = '000'

    expected_char_judgment = (False, '00', '110')

    actual = self.encoding_under_test.judge_bits(guess, win)
    self.assertFalse(actual.correct)
    self.assertEqual(guess, actual.correct_guess)
    self.assertEqual(1, len(actual.char_judgments))
    self.assertEqual(expected_char_judgment, actual.char_judgments[0])


if __name__ == '__main__':
  unittest.main()
