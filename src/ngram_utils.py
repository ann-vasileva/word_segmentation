import math
from collections import defaultdict

def load_bigrams(filepath):
    '''
    count bigrams based on freqeunces precalculated from opencorpora
    '''
    bigram_probs = defaultdict(float)
    total_count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                w1, w2, count, doc_freq = parts
                w1, w2 = w1.replace("ё", "е"), w2.replace("ё", "е")
                count = int(count)
                bigram_probs[(w1, w2)] = count
                total_count += count
    for bigram in bigram_probs:
        bigram_probs[bigram] = math.log(bigram_probs[bigram] / total_count)
    return bigram_probs

def load_unigrams(filepath):
    '''
    count unigrams based on freqeunces precalculated from opencorpora
    '''
    unigram_probs = defaultdict(float)
    total_count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                w1, count, doc_freq = parts
                count = int(count)
                unigram_probs[w1] = count
                total_count += count
    for unigram in unigram_probs:
        unigram_probs[unigram] = math.log(unigram_probs[unigram] / total_count)
    return unigram_probs

