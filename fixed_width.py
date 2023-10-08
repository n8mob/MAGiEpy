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

        trailing_bit_length = len(guess_bits) % self.width
        if trailing_bit_length > 0:
            guess_bits = guess_bits[:-trailing_bit_length]

        for char_index in range(0, min(len(guess_bits), len(win_bits)), self.width):
            char_judgment = ''
            char_correct = True
            for bit_index in range(char_index, char_index + self.width):
                if guess_bits[bit_index] == win_bits[bit_index]:
                    char_judgment += '1'
                else:
                    char_judgment += '0'
                    char_correct = False
                    all_correct = False

            if char_correct:
                correct_full_guess += guess_bits[char_index:char_index+self.width]
            else:
                if not guess_bits:
                    char_judgment = '0' * self.width

            char_judgements.append(CharJudgment(char_correct, guess_bits[char_index:char_index + self.width], char_judgment))

        return FullJudgment(all_correct, correct_full_guess, char_judgements)
