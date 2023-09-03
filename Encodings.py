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

    def encode_bit_string(self, c) -> str:
        """
        given a character, encode it and return the bits as a string of 1's and 0's
        Args:
            c: character to decode

        Returns: a string of 1's and 0's representing the binary encoding of the given character

        """
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

    def decode_bit_string(self, bit_string):
        dec = ''
        if bit_string:
            if isinstance(bit_string, list):
                bit_string = ''.join(bit_string)

            for char_index in range(0, len(bit_string), self.width):
                enc = int(bit_string[char_index:char_index + self.width], 2)
                dec += self.decode(enc)
        else:
            dec = self.decode(self.default_encoded)
        return dec

    def encode_bit_string(self, c):
        b = self.encode(c)

        return f'{self.encode(c) :0{self.width}b}'
