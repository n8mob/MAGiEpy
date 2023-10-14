from binary_encoding import BinaryEncoding
from judgments import FullJudgment, CharJudgment


class FixedWidthEncoding(BinaryEncoding):
    def __init__(self, width, encoding: dict, decoding: dict = None, default_encoded=0, default_decoded='?'):
        super().__init__('fixed')
        self.encoding = encoding
        self.decoding = decoding or {v: k for k, v in self.encoding.items()}
        self.default_encoded = default_encoded
        self.default_decoded = default_decoded
        self.width = width

    def decode(self, enc):
        return self.decoding[enc] if enc in self.decoding else self.default_decoded

    def encode(self, c):
        return self.encoding[c] if c in self.encoding else self.default_encoded

    def decode_bit_string(self, bit_string):
        dec = ''
        if bit_string:
            if isinstance(bit_string, list):
                for char_string in bit_string:
                    enc = int(char_string, 2)
                    dec += self.decode(enc)
            else:
                for char_index in range(0, len(bit_string), self.width):
                    enc = int(bit_string[char_index:char_index + self.width], 2)
                    dec += self.decode(enc)
        return dec

    def encode_bit_string(self, s):
        b = ''
        for c in s:
            b += f'{self.encode(c) :0{self.width}b}'

        return b

    def judge_bits(self, guess_bits, win_bits) -> FullJudgment:
        all_correct = len(guess_bits) == len(win_bits)
        correct_full_guess = ''

        char_judgements = []
        split_guess = self.split_bitstring(guess_bits)
        split_win = self.split_bitstring(win_bits)

        for char_index in range(0, min(len(split_guess), len(split_win))):
            char_judgment = ''
            char_correct = True
            guess_char_bits = split_guess[char_index]
            win_char_bits = split_win[char_index]
            for bit_index in range(0, self.width):
                if guess_char_bits[bit_index] == win_char_bits[bit_index]:
                    char_judgment += '1'
                else:
                    char_judgment += '0'
                    char_correct = False
                    all_correct = False

            if char_correct:
                correct_full_guess += guess_char_bits
            else:
                if not split_guess:
                    char_judgment = '0' * self.width

            char_judgements.append(CharJudgment(char_correct, guess_char_bits, char_judgment))

        return FullJudgment(all_correct, correct_full_guess, char_judgements)

    def split_bitstring(self, bitstring):
        trailing_bit_length = len(bitstring) % self.width
        if trailing_bit_length > 0:
            bitstring = bitstring[:-trailing_bit_length]

        split = []
        for char_index in range(0, len(bitstring), self.width):
            split.append(bitstring[char_index:char_index+self.width])
        return split


    def judge_text(self, guess_text, win_text) -> FullJudgment:
        all_correct = len(guess_text) == len(win_text)
        guess_while_correct = ''
        correct_so_far = True

        char_judgments = []

        for char_index in range(0, min(len(guess_text), len(win_text))):
            guess_char = guess_text[char_index]
            char_correct = guess_char == win_text[char_index]
            all_correct = all_correct and char_correct
            correct_so_far = correct_so_far and char_correct
            if correct_so_far:
                guess_while_correct += guess_char

            char_judgments.append(CharJudgment(char_correct, guess_char, '1' if char_correct else '0'))

        return FullJudgment(all_correct, guess_while_correct, char_judgments)

