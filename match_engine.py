from __future__ import print_function
import jellyfish
import ngram
import automata
import bisect
from matcher import Matcher

class MatchEngine(object):
    def __init__(self, dicts):
        self.dicts = dicts

    def find_match_levenshtein(self, token, canonical):
        candidates = []
        best_score = 1
        for word in self.dicts:
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

    def find_match_jaro_winkler(self, token, canonical):
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

        best_match = ""

        return match_metaphone, is_match, best_match

    def find_match_levenshtein_automaton(self, token, canonical):
        m = Matcher(self.dicts)
        candidates = list(automata.find_all_matches(token, 2, m))
        # fetch metaphone for token
        token_metaphone = jellyfish.metaphone(token)
        match_metaphones = [match for match in candidates if jellyfish.metaphone(
            match.decode("utf-8")) == token_metaphone]

        is_match = False
        for word in match_metaphones:
            if word == canonical:
                is_match = True
                break

        return match_metaphones, is_match, ""
