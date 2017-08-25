import pprint
import ngram

#labelled_token = open('data/labelled-tokens.txt', 'r')

DICT_PATH = 'data/dict.txt'
LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

results = []
dict_list = [line.strip() for line in open(DICT_PATH, 'r')]
G = ngram.NGram(dict_list)

with open(LABELLED_TOKEN_PATH,'r') as tokens:
    for token in tokens:
        split_token = token.split('\t')
        print(G.search('plays', threshold=0.4))

def soundex(name, len=4):
    """ soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen
        public domain
    """

    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''

    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d

    # replace first digit with first alpha character
    sndx = fc + sndx[1:]

    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')

    # return soundex code padded to len characters
    return (sndx + (len * '0'))[:len]
