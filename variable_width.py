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
