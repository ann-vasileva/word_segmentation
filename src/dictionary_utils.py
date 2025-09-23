from collections import Counter
import re
from tqdm import tqdm

class TrieNode:
    '''
    Simple data class for the efficient words search
    '''
    def __init__(self):
        self.children = {}
        self.is_word = False

def extract_wordforms(filepath):
    '''
    Extract words from Opencorpora corpus
    '''
    wordforms = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if re.fullmatch(r"\d+", line): #skip digits
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                form, _ = parts
                form = form.lower().replace("ё", "е") #change tricky "ё" that almost nobody uses
                wordforms.append(form)
    return sorted(set(wordforms))

def extend_dictionary(avito_texts, min_freq=5, top_k=1000): 
    '''
    Enrich opencorpora dictionary with top specific domain words from Avito 
    '''
    all_tokens = []
    for col in ["cand_title", "base_title"]: #use item titles for better phrasing, they capture all necessary words like brands or appliances ("Xbox One", "мультиварка")
        for text in tqdm(avito_texts[col]):
            tokens = re.findall(r"[а-яА-ЯёЁa-zA-Z]+", text.lower())
            all_tokens.extend(tokens)
    freq = Counter(all_tokens)
    new_words = [w for w, c in freq.items() if c >= min_freq and len(w) >= 2]
    return sorted(new_words, key=lambda w: -freq[w])[:top_k]

def build_trie(words):
    '''
    Build a trie based on the initial dictionary to search for words efficiently
    Speedups prepocessing from 7 seconds per sentence (very slow) to instant performance
    '''
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True
    return root

