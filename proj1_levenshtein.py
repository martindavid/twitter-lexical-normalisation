from __future__ import print_function
import jellyfish
import time
import json
import ngram


def find_match(token, canonical, dicts):
    candidates = []
    best_score = 1
    for word in dicts:
        score = jellyfish.levenshtein_distance(
            token, word.decode("utf-8").lower())
        if score <= best_score:
            best_score = score
            candidates.append(word.lower())

    token_metaphone = jellyfish.metaphone(token.decode("utf-8"))
    match_metaphone = [match for match in candidates if jellyfish.metaphone(
        match.decode("utf-8")) == token_metaphone]

    G = ngram.NGram(match_metaphone)
    best_candidates = G.search(token, threshold=0.5)

    is_match = False
    for word in match_metaphone:
        if word == canonical:
            is_match = True
            break

    if len(best_candidates) > 0:
        best_match = best_candidates[0][0]
    else:
        best_match = ""

    return match_metaphone, is_match, best_match


def dump_to(data, file_name):
    with open(file_name, 'w') as fout:
        json.dump(data, fout)


results = []
DICT_PATH = 'data/words.txt'
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

        candidates, is_match, match_word = find_match(
            token_word, canonical, DICTS)
        result = {
            'token': token_word,
            'candidates': candidates,
            'canonical': canonical,
            'is_correct': is_match,
            'match_word': match_word
        }

        results.append(result)
        print(result)
        count += 1

dump_to(results, "output/levenshtein_1.json")

total_minutes = time.time() - start_time
minutes, seconds = divmod(total_minutes, 60)
print("\nTotal time used for execution is %02d minutes and %02d seconds" %
      (minutes, seconds))
