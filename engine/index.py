import os
import hashlib
import itertools
import string
import json

def create_index_folder():
    if not os.path.exists("_INDEX"):
        os.mkdir("_INDEX")

def full_text_index(text):
    indices = [text]
    text = text.split()
    for i, word in enumerate(text):
        for j in range(1, len(text)):
            if i + j <= len(text):
                indices.append(' '.join(text[i:i + j]))
    return indices

def index(text, obj):
    create_index_folder()

    indices = set()
    text = text.lower().strip()
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    text = ' '.join(text.split())

    for index in full_text_index(text):
        indices.add(index)
    
    for index in indices:
        file = os.path.join("_INDEX", hashlib.md5(index.encode()).hexdigest())
        data = []
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump([], f)
        else:
            with open(file) as f:
                data = json.load(f)
        
        data.append(obj)
        with open(file, 'w') as f:
            json.dump(data, f)
