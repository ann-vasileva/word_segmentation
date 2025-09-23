import re

def split_on_heuristics(text):
    '''
    A very simple function to split the sentence based on obvious, yet effective rules:
    1. Add space after punctuation
    2. Handle single uppercase Russian letters
    3. Latin letters touch Cyrillic letters, insert a space between them.
    4. Split digits and letters      
    '''
    text = re.sub(r'([.,!?;:-])', r'\1 ', text)
    text = re.sub(r'([a-zA-Z])([а-яА-Я])', r'\1 \2', text)
    text = re.sub(r'([а-яА-Я])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Zа-яА-Я])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Zа-яА-Я])(\d)', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

