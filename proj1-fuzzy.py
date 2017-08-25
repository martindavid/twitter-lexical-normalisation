from fuzzywuzzy import fuzz, process

DICT_PATH = 'data/dict.txt'
LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

results = []
dict_list = [line.strip() for line in open(DICT_PATH, 'r')]

with open(LABELLED_TOKEN_PATH, 'r') as tokens:
    for token in tokens:
        split_token = token.split('\t')
        search_token = split_token[0].strip()
        code = split_token[1]
        canonical = split_token[2].strip()

        if code != 'NO':
            best_score = 0
            best_string = ""
            for word in dict_list:
                score = fuzz.ratio(search_token, word)
                if score > best_score:
                    best_score = score
                    best_string = word

            print("%s,%s,%s,%d,%s,%r" %
                  (code, search_token, best_string, best_score, canonical, canonical == best_string))

            result = {
                "token": search_token,
                "match": best_string,
                "score": best_score,
                "canonical": canonical,
                "is_correct": best_string == canonical
            }
            results.append(result)
