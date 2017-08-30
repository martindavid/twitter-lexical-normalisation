from __future__ import print_function
import jellyfish
import time

DICT_PATH = 'data/dict.txt'
LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

DICTS = [line.strip() for line in open(DICT_PATH, 'r')]


def find_match_levenshtein(token, dicts):
    candidates = []
    best_match = ""
    best_score = 2.1
    for word in dicts:
        score = jellyfish.levenshtein_distance(
            unicode(token, "utf-8"), unicode(word, "utf-8"))
        if score <= 2 and score < best_score:
            best_score = score
            best_match = word
            candidates.append(word)

    return candidates, best_match


def find_match_damerau_levenshtein(token, dicts):
    candidates = []
    best_match = ""
    best_score = 3
    for word in dicts:
        score = jellyfish.damerau_levenshtein_distance(
            unicode(token, "utf-8"), unicode(word, "utf-8"))
        if score <= 2 and score < best_score:
            best_score = score
            best_match = word
            candidates.append({
                'word': word,
                'score': best_score
            })

    return candidates, best_match


def find_match_jaro(token, dicts):
    candidates = []
    best_match = ""
    best_score = 0.75
    for word in dicts:
        score = jellyfish.jaro_winkler(
            unicode(token, "utf-8"), unicode(word, "utf-8"))
        if score >= 0.75 and score > best_score:
            best_score = score
            best_match = word
            candidates.append({
                'word': word,
                'score': round(best_score, 2)
            })

    return candidates, best_match

start_time = time.time()
with open(LABELLED_TOKEN_PATH, 'r') as tokens:
    for token in tokens:
        split_token = token.split('\t')
        token_word = split_token[0].strip()
        code = split_token[1]
        canonical = split_token[2].strip()

        candidates, match_word = find_match_levenshtein(token_word, DICTS)
        result = {
            'token': token_word,
            'candidates': candidates,
            'match': match_word,
            'canonical': canonical,
            'is_correct': match_word == canonical
        }

        total_minutes = time.time() - start_time
        minutes, seconds = divmod(total_minutes, 60)
        print(result)

print("\nTotal time used for execution is %02d minutes and %02d seconds" % (minutes, seconds))
