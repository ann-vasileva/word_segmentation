from collections import defaultdict
from .preprocessing import split_on_heuristics
from .utils import remove_punctuation, restore_punctuation, finalize_dashes

def segment_text_fast(text, trie, bigram_probs, uniram_probs, max_word_len=30):
    '''
    Segmentation algorithm based on the probabilistic model 
    '''
    raw_text, posit = remove_punctuation(text) # remove tricky punctuation to help ngrams split words (empirical observation)
    raw_text = split_on_heuristics(raw_text) #use heuristics to split obsvious cases like 'холодильникSamsung'
    segments = raw_text.split() # work with detected chunks to speed-up the process
    result = []

    for seg in segments:
        n = len(seg) #initialzie dynamics for the current chunck
        dp = [-float('inf')] * (n + 1)
        dp[0] = 0
        backtrace = [0] * (n + 1)
        prev_word = [""] * (n + 1)

        for i in range(n): #
            if dp[i] == -float('inf'):
                continue
            node = trie
            for j in range(i, min(n, i + max_word_len)): # check the next symbols
                ch = seg[j].lower()
                if ch == "ё": # to avoid not finding word in the dictionary
                    ch = "е"
                if ch not in node.children:
                    break
                node = node.children[ch]
                if node.is_word:
                    word = seg[i:j+1].lower()
                    bigram_score = bigram_probs.get((prev_word[i], word), -25.0) if i > 0 else uniram_probs.get(word, -25.0) #check probabilities
                    score = dp[i] + bigram_score
                    if score > dp[j+1]:
                        dp[j+1] = score
                        backtrace[j+1] = i
                        prev_word[j+1] = word
        words, i = [], n
        while i > 0:
            j = backtrace[i]
            words.append(seg[j:i])
            i = j
        words.reverse()
        result.extend(words)

    result = " ".join(result)
    result = restore_punctuation(result, posit)
    result = finalize_dashes(result)
    return result

