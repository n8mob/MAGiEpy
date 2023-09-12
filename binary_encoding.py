class BinaryEncoding:
    def __init__(self, encoding_type):
        self.encoding_type = encoding_type

    def decode(self, enc):
        pass

    def encode(self, c):
        pass

    def decode_bit_string(self, bit_string):
        pass

    def encode_bit_string(self, c) -> str:
        """
        given a character, encode it and return the bits as a string of 1's and 0's
        Args:
            c: character to decode

        Returns: a string of 1's and 0's representing the binary encoding of the given character

        """
        pass

    @staticmethod
    def judge_bits(guess_bits, win_bits):
        all_correct = True
        judgement = ''
        for bit_index in range(min(len(guess_bits), len(win_bits))):
            if guess_bits[bit_index] == win_bits[bit_index]:
                judgement += '1'
            else:
                judgement += '0'
                all_correct = False

        return all_correct, judgement
