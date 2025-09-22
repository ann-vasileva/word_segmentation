import re

def split_on_heuristics(text):
    text = re.sub(r'([.,!?;:-])', r'\1 ', text)
    text = re.sub(r'(?<!-^)([А-Я]{2,})', lambda m: ' ' + m.group(1).capitalize(), text)
    text = re.sub(r'(?<!-^)([А-Я])', r' \1', text)
    text = re.sub(r'([a-zA-Z])([а-яА-Я])', r'\1 \2', text)
    text = re.sub(r'([а-яА-Я])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Zа-яА-Я])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Zа-яА-Я])(\d)', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

