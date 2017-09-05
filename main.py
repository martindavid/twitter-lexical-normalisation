from __future__ import print_function
import argparse
import logging
import json
import time
import io
from match_engine import MatchEngine


def dump_to(data, file_name):
    with open(file_name, 'w') as fout:
        json.dump(data, fout)


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    method = args.method
    filename = args.filename
    dict_path = args.dictionary

    labelled_token_path = 'data/labelled-tokens.txt'

    dicts = [line.strip() for line in open(dict_path, 'r')]

    results = []
    start_time = time.time()
    with io.open(labelled_token_path, 'r', encoding='ISO-8859-1') as tokens:
        count = 0
        for token in tokens:
            if count > 1000:
                break
            try:
                split_token = token.split('\t')
                token_word = unicode(split_token[0].strip())
                code = split_token[1]
                canonical = split_token[2].strip()
                engine = MatchEngine(dicts)

                if code == 'OOV':
                    if method == "0":  # levenshtein only
                        candidates, is_match = engine.find_match_levenshtein(
                            token_word, canonical)
                    elif method == "1":  # levenshtein + soundex method
                        candidates, is_match = engine.find_match_levenshtein_soundex(
                            token_word, canonical)
                    else:  # levenshtein + metaphone method
                        candidates, is_match  = engine.find_match_levenshtein_metaphone(
                            token_word, canonical)

                    result = {
                        'token': token_word,
                        'candidates': candidates,
                        'canonical': canonical,
                        'is_correct': is_match,
                        'code': code,
                        'candidates_len': len(candidates)
                    }

                    results.append(result)
                    print(result)
            except Exception:
                continue

            count += 1

    dump_to(results, filename)

    total_minutes = time.time() - start_time
    minutes, seconds = divmod(total_minutes, 60)
    print("\nTotal time used for execution is %02d minutes and %02d seconds" %
          (minutes, seconds))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="A CLI app to for lexical twitter",
        fromfile_prefix_chars='@')

    PARSER.add_argument(
        "-d",
        "--dictionary",
        help="Dictionary path",
        required=True
    )

    PARSER.add_argument(
        "-m",
        "--method",
        help="String matching algorithm method [0 - levenshtein, 1 - levenshtein + soundex, 2 - levenshtein + metaphone]",
        metavar="METHOD",
        required=True
    )

    PARSER.add_argument(
        "-f",
        "--filename",
        help="Filename for a dump file",
        metavar="FILENAME",
        required=True
    )

    PARSER.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")

    ARGS = PARSER.parse_args()

    # Setup logging
    if ARGS.verbose:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    main(ARGS, LOG_LEVEL)
