import ngram

DICTS = [line.strip() for line in open('data/words.txt', 'r')]
G = ngram.NGram(DICTS)

print(G.search('comming', threshold=0.75))