from binary_encoding import BinaryEncoding
from judgments import CharJudgment, FullJudgment


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

        bit_string = ''
        for decoded_symbol in decoded_symbols:
            bit_string += decoded_symbol or ''

        return bit_string


    def split_by_switch(self, bit_string):
        split_encoded = []
        switch_indexes = [0]
        for i in range(1, len(bit_string)):
            if bit_string[i - 1] != bit_string[i]:
                switch_indexes.append(i)
                next_char = bit_string[switch_indexes[-2]:switch_indexes[-1]]
                if next_char != self.character_separator:
                    split_encoded.append(next_char)

        last_char = bit_string[switch_indexes[-1]:]

        if last_char != self.character_separator:
            split_encoded.append(last_char)

        return split_encoded

    def judge_bits(self, guess_bits, win_bits) -> FullJudgment:
        char_judgments = []

        guess_chars = self.split_by_switch(guess_bits)
        win_chars = self.split_by_switch(win_bits)

        if len(guess_chars) > len(win_chars):
            char_len = len(win_chars)
        else:
            char_len = len(guess_chars)

        correct_guess_chars = []
        correct_so_far = True
        all_correct = char_len == len(win_chars)

        for char_index in range(char_len):
            guess_char = guess_chars[char_index]
            win_char = win_chars[char_index]
            char_judgment = ''

            if len(guess_char) > len(win_char):
                shorter = win_char
                longer = guess_char
            else:
                shorter = guess_char
                longer = win_char

            char_correct = True
            partial_correct = ''

            for bit_index in range(len(longer)):
                if bit_index < len(shorter) and shorter[bit_index] == longer[bit_index]:
                    char_judgment += '1'
                    partial_correct += shorter[bit_index]
                else:
                    char_judgment += '0'
                    char_correct = False
                    correct_so_far = False
                    if partial_correct:
                        correct_guess_chars.append(partial_correct)
                    break

            all_correct = all_correct and char_correct

            if correct_so_far and char_correct:
                correct_guess_chars.append(guess_char)

            char_judgments.append(CharJudgment(char_correct, guess_char, char_judgment))

        return FullJudgment(all_correct, self.join(correct_guess_chars), char_judgments)

    def join(self, chars):
        if not chars:
            return ''

        joined = chars[0]
        for char_index in range(1, len(chars)):
            previous_char = chars[char_index - 1]
            current_char = chars[char_index]
            if current_char[0] != self.character_separator and previous_char[0] != self.character_separator:
                joined += self.character_separator
            joined += current_char

        return joined
