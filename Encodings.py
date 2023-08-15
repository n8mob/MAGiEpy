

class FixedWidthEncoder:
    def __init__(self, bit_width, encoding: dict, decoding:dict=None, default_decoded='?', default_encoded=0):
        self.width = bit_width
        self.encoding = encoding
        self.decoding = decoding or {v: k for k, v in encoding.items()}
        self.default_decoded = default_decoded
        self.default_encoded = default_encoded

    def decode(self, enc):
        return self.decoding[enc] if enc in self.decoding else self.default_decoded

    def encode(self, c):
        return self.encoding[c] if c in self.encoding else self.default_encoded

    def encode_bit_string(self, c):
        b = self.encode(c)

        return f"{self.encode(c):05b}"

    def decode_bit_string(self, b):
        pass