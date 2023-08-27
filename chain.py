import string

keyWords = {'THE': '-',
            'A': '--',
            'AN': '--',
            'OF': '---',
            'TO': '----',
            }

def encodeSentence(sentence):
    sentence = ''.join(c for c in sentence.replace('-', ' ') if c not in string.punctuation).upper()
    return '--'.join([encodeWord(w) for w in sentence.split()])


def encodeWord(word):
    word = word.upper()
    if word in keyWords:
        return keyWords[word]
    else:
        return '-'.join(encodeLetter(l) for l in word)

    
def encodeLetter(letter):
    letter = letter.upper()
    count = ord(letter[0]) - 64
    return '|' * count
    
