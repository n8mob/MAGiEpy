class Encoding:
    def decode(self, enc):
        pass

    def encode(self, c):
        pass


class BinaryEncoding(Encoding):
    def __init__(self, width: int):
        self.width = width

    def decode_bit_string(self, b):
        pass

    def encode_bit_string(self, c):
        pass


class FixedWidthEncoding(BinaryEncoding):
    def __init__(self, width, encoding: dict, decoding: dict = None, default_decoded='?', default_encoded=0):
        super().__init__(width)
        self.encoding = encoding
        self.decoding = decoding or {v: k for k, v in encoding.items()}
        self.default_decoded = default_decoded
        self.default_encoded = default_encoded

    def decode(self, enc):
        return self.decoding[enc] if enc in self.decoding else self.default_decoded

    def encode(self, c):
        return self.encoding[c] if c in self.encoding else self.default_encoded

    def decode_bit_string(self, b):
        enc = int(''.join(b), 2)
        return self.decode(enc)

    def encode_bit_string(self, c):
        b = self.encode(c)

        return f'{self.encode(c) :0{self.width}b}'
