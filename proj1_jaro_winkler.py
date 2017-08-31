from __future__ import print_function
import jellyfish
import time
import json
import automata

def find_match(token, canonical, dicts):
    candidates = []
    best_score = 0.75
    for word in dicts:
        score = jellyfish.jaro_winkler(token, word.decode("utf-8"))
        if score > best_score:
            best_score = score
            candidates.append(word)

    token_metaphone = jellyfish.metaphone(token.decode("utf-8"))
    match_metaphone = [match for match in candidates if jellyfish.metaphone(
        match.decode("utf-8")) == token_metaphone]

    is_match = False
    for word in match_metaphone:
        if word == canonical:
            is_match = True
            break

    return match_metaphone, is_match

def dump_to(data, file_name):
    with open(file_name, 'w') as fout:
        json.dump(data, fout)

results = []
DICT_PATH = 'data/wlist_match2.txt'
LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

DICTS = [line.strip() for line in open(DICT_PATH, 'r')]

start_time = time.time()
with open(LABELLED_TOKEN_PATH, 'r') as tokens:
    count = 0
    for token in tokens:
        if count > 400:
            break

        split_token = token.split('\t')
        token_word = split_token[0].decode("utf-8").strip()
        code = split_token[1]
        canonical = split_token[2].strip()

        candidates, is_match = find_match(token_word, canonical, DICTS)
        result = {
            'token': token_word,
            'candidates': candidates,
            'canonical': canonical,
            'is_correct': is_match
        }

        results.append(result)
        print(result)
        count += 1

dump_to(results, "output/distance_result_2.json")

total_minutes = time.time() - start_time
minutes, seconds = divmod(total_minutes, 60)
print("\nTotal time used for execution is %02d minutes and %02d seconds" % (minutes, seconds))
