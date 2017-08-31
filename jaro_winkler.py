from __future__ import print_function
import jellyfish
import time
import json
import automata

class JaroWinkler(object):
    def __init__(self, dicts):
        self.dicts = dicts

    def find_match(self, token, canonical):
        candidates = []
        best_score = 0.75
        for word in self.dicts:
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
