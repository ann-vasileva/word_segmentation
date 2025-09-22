import string
from collections import defaultdict
import re

def remove_punctuation(text):
    positions, result_chars = [], []
    clean_index = 0
    for ch in text:
        if (ch in string.punctuation or ch in "«»—–“”’") and ch != " ":
            positions.append((clean_index, ch))
        else:
            result_chars.append(ch)
            clean_index += 1
    return "".join(result_chars), positions

def restore_punctuation(text, positions):
    result = []
    pos_dict = defaultdict(list)
    for idx, sym in positions:
        pos_dict[idx].append(sym)
    i_orig = 0
    for ch in text:
        if i_orig in pos_dict:
            result.extend(pos_dict.pop(i_orig))
        result.append(ch)
        if ch != " ":
            i_orig += 1
    while i_orig in pos_dict:
        result.extend(pos_dict[i_orig])
        i_orig += 1
    return "".join(result)

def finalize_dashes(text):
    return re.sub(r'\s*([—–])\s*', r'\1', text)

def get_space_indices(text):
    positions = []
    offset = 0
    for i, ch in enumerate(text):
        if ch == ' ':
            positions.append(i + offset)
            offset -= 1
    return str(positions)

