import re, collections

def words(text):
    found = re.findall('[a-z]+', text.lower())
    return found


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('data/dict.txt').read()))

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces = [a + c + b[1:] for a, b in s for c in letters if b]
    inserts = [a + c + b     for a, b in s for c in letters]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    print(candidates)
    return max(candidates, key=NWORDS.get)

with open('data/labelled-tokens.txt','r') as tokens:
    for token in tokens:
        split_token = token.split('\t')
        token_word = split_token[0]
        code = split_token[1]
        if code != 'IV':
            print("token: %s - match: %s" % (token_word, correct(token_word)))
