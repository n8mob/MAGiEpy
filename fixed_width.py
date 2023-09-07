from binary_encoding import BinaryEncoding


class FixedWidthEncoding(BinaryEncoding):
    def __init__(self, width, encoding: dict, decoding: dict = None, default_encoded=0, default_decoded='?'):
        self.encoding = encoding
        self.decoding = decoding or {v: k for k, v in self.encoding.items()},
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
        else:
            dec = self.decode(self.default_encoded)
        return dec

    def encode_bit_string(self, s):
        b = []
        for c in s:
            b.append(f'{self.encode(c) :0{self.width}b}')

        return b
