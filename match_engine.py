from __future__ import print_function
import jellyfish
#import ngram

class MatchEngine(object):
    def __init__(self, dicts):
        self.dicts = dicts

    def find_match_levenshtein(self, token, canonical):
        candidates = []
        best_score = 2
        for word in self.dicts:
            score = jellyfish.levenshtein_distance(
                token, word.decode("utf-8").lower())
            if score <= best_score:
                best_score = score
                candidates.append(word.lower())

        #G = ngram.NGram(candidates)
        #best_candidates = G.search(token, threshold=0.5)

        #results = [item[0] for item in best_candidates]

        is_match = False
        for word in candidates:
            if word == canonical:
                is_match = True
                break

        #if len(best_candidates) > 0:
        #    best_match = best_candidates[0][0]
        #else:
        #    best_match = ""

        return candidates, is_match


    def find_match_levenshtein_soundex(self, token, canonical):
        candidates = []
        best_score = 2
        for word in self.dicts:
            score = jellyfish.levenshtein_distance(
                token, word.decode("utf-8").lower())
            if score <= best_score:
                best_score = score
                candidates.append(word.lower())

        token_soundex = jellyfish.soundex(token.decode("utf-8"))
        match_soundex = [match for match in candidates if jellyfish.soundex(
            match.decode("utf-8")) == token_soundex]

        #G = ngram.NGram(match_soundex)
        #best_candidates = G.search(token, threshold=0.5)

        #results = [item[0] for item in best_candidates]

        is_match = False
        for word in match_soundex:
            if word == canonical:
                is_match = True
                break

        #if len(best_candidates) > 0:
        #    best_match = best_candidates[0][0]
        #else:
        #    best_match = ""

        return match_soundex, is_match

    def find_match_levenshtein_metaphone(self, token, canonical):
        candidates = []
        best_score = 2
        for word in self.dicts:
            score = jellyfish.levenshtein_distance(
                token, word.decode("utf-8").lower())
            if score <= best_score:
                best_score = score
                candidates.append(word.lower())

        token_metaphone = jellyfish.metaphone(token.decode("utf-8"))
        match_metaphone = [match for match in candidates if jellyfish.metaphone(
            match.decode("utf-8")) == token_metaphone]

        #G = ngram.NGram(match_metaphone)
        #best_candidates = G.search(token, threshold=0.5)

        #results = [item[0] for item in best_candidates]

        is_match = False
        for word in match_metaphone:
            if word == canonical:
                is_match = True
                break

        #if len(best_candidates) > 0:
        #    best_match = best_candidates[0][0]
        #else:
        #    best_match = ""

        return match_metaphone, is_match
