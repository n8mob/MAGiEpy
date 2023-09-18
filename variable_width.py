from binary_encoding import BinaryEncoding


class VariableWidthEncoding(BinaryEncoding):
    def __init__(
            self,
            encoding: dict[str, dict],
            decoding: dict = None,
            default_encoded='1',
            default_decoded='0',
            character_separator='0',
            word_separator='00'
            ):
        super().__init__('variable')
        self.encoding = encoding
        self.decoding = decoding or {
            bit: {v: k for k, v in self.encoding[bit].items()}
            for bit in self.encoding
        }
        self.default_encoded = default_encoded
        self.default_decoded = default_decoded
        self.character_separator = character_separator
        self.word_separator = word_separator

    def encode(self, c):
        if c in self.encoding['1']:
            return self.encoding['1'][c]
        elif c in self.encoding['0']:
            return self.encoding['0'][c]
        else:
            return self.default_encoded

    def decode(self, enc):
        if enc in self.decoding['1']:
            return self.decoding['1'][enc]
        elif enc in self.decoding['0']:
            return self.decoding['0'][enc]

    def encode_bit_string(self, s: str) -> str:
        encoded_words = []
        for word in s.split(' '):
            encoded_characters = []
            for c in word:
                encoded_characters.append(self.encode(c))
            encoded_words.append(self.character_separator.join(encoded_characters))

        return self.word_separator.join(encoded_words)

    def decode_bit_string(self, bit_string):
        split_encoded = self.split_by_switch(bit_string)
        decoded_symbols = [self.decode(symbol) for symbol in split_encoded]
        return ''.join(decoded_symbols)

    @staticmethod
    def split_by_switch(bit_string):
        split_encoded = []
        switch_indexes = [0]
        for i in range(1, len(bit_string)):
            if bit_string[i - 1] != bit_string[i]:
                switch_indexes.append(i)
                split_encoded.append(bit_string[switch_indexes[-2]:switch_indexes[-1]])

        split_encoded.append(bit_string[switch_indexes[-1]:])

        return split_encoded

    def judge_bits(self, guess_bits, win_bits):
        all_correct = True
        full_judgement = []

        guess_chars = self.split_by_switch(guess_bits)
        win_chars = self.split_by_switch(win_bits)

        if len(guess_chars) > len(win_chars):
            all_correct = False
            char_len = len(win_chars)
        else:
            char_len = len(guess_chars)

        for char_index in range(char_len):
            guess_char = guess_chars[char_index]
            win_char = win_chars[char_index]
            char_judgement = ''

            if len(guess_char) > len(win_char):
                char_correct = False
                bit_len = len(win_char)
            else:
                char_correct = True
                bit_len = len(guess_char)

            for bit_index in range(bit_len):
                if guess_bits[bit_index] == win_bits[bit_index]:
                    char_judgement += '1'
                else:
                    char_judgement += '0'
                    char_correct = False

            all_correct = all_correct and char_correct

            full_judgement.append((char_correct, guess_char, char_judgement))

        return all_correct, guess_chars, full_judgement
