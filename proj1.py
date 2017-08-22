import pprint
import editdistance
from subprocess import call

#labelled_token = open('data/labelled-tokens.txt', 'r')

DICT_PATH = 'data/dict.txt'
LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

results = []
dict_list = [line.strip() for line in open(DICT_PATH, 'r')]

labelled_token = open(LABELLED_TOKEN_PATH)
count = 0


for tokens in labelled_token:
    split_tokens = tokens.split('\t')
    search_token = split_tokens[0].strip()
    token_code = split_tokens[1]
    canonical = split_tokens[2].strip()

    result = {
        'token': search_token,
        'match_word': "",
        'canonical': split_tokens[2],
        'match_score': 0,
        'is_correct': False
    }

    best_score = 999999999999
    best_match = ""

    for word in dict_list:
        score = editdistance.eval(search_token, word)
        if score < best_score:
            best_score = score
            best_match = word

    result['match_word'] = best_match
    result['match_score'] = best_score
    result['is_correct'] = best_match == canonical
    print(result)
    results.append(result)