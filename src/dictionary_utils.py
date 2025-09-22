from collections import Counter
import re
from tqdm import tqdm

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

def extract_wordforms(filepath):
    wordforms = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if re.fullmatch(r"\d+", line):
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                form, _ = parts
                form = form.lower().replace("ё", "е")
                wordforms.append(form)
    return sorted(set(wordforms))

def extend_dictionary(avito_texts, min_freq=5, top_k=1000):
    all_tokens = []
    for col in ["cand_title", "base_title"]:
        for text in tqdm(avito_texts[col]):
            tokens = re.findall(r"[а-яА-ЯёЁa-zA-Z]+", text.lower())
            all_tokens.extend(tokens)
    freq = Counter(all_tokens)
    new_words = [w for w, c in freq.items() if c >= min_freq and len(w) >= 2]
    return sorted(new_words, key=lambda w: -freq[w])[:top_k]

def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True
    return root

