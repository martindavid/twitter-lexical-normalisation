import bisect
import automata
import jellyfish
import json
import time

class Matcher(object):
    def __init__(self, l):
        self.l = l
        self.probes = 0

    def __call__(self, w):
        self.probes += 1
        pos = bisect.bisect_left(self.l, w)
        if pos < len(self.l):
            return self.l[pos]
        else:
            return None

def find_match(token, canonical, m):
    candidates = list(automata.find_all_matches(token, 1, m))
    # fetch metaphone for token
    token_metaphone = jellyfish.metaphone(token)
    match_metaphones = [match for match in candidates if jellyfish.metaphone(
        match.decode("utf-8")) == token_metaphone]

    is_match = False
    for word in match_metaphones:
        if word == canonical:
            is_match = True
            break

    return match_metaphones, is_match


def dump_to(data, file_name):
    with open(file_name, 'w') as fout:
        json.dump(data, fout)


DICTS = [line.strip() for line in open('data/wlist_match2.txt', 'r')]
m = Matcher(DICTS)
results = []
start_time = time.time()
with open('data/labelled-tokens.txt', 'r') as f:
    count = 0
    for line in f:
        split_token = line.split('\t')
        if count <= 400:
            token_word = split_token[0].decode("utf-8")
            canonical = split_token[2].decode("utf-8").strip()
            candidates, is_match = find_match(token_word, canonical, m)
            result = {
                "token": token_word,
                "canonical": canonical,
                "candidates": candidates,
                "is_match": is_match
            }
            print(result)
            results.append(result)
        count += 1
    
dump_to(results, 'output/automaton_result.json')
total_minutes = time.time() - start_time
minutes, seconds = divmod(total_minutes, 60)
print("\nTotal time used for execution is %02d minutes and %02d seconds" % (minutes, seconds))
