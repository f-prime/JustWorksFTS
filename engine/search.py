import hashlib
import string
import os
import json
from engine.index import full_text_index

def search(text):
    text = text.lower().strip()
    for char in string.punctuation:
        text = text.replace(char, '')
    
    check = hashlib.md5(text.encode()).hexdigest()
    if os.path.exists(os.path.join("_INDEX", check)):
        with open(os.path.join("_INDEX", check)) as f:
            return json.load(f)
    else:
        possible = full_text_index(text)
        for index in possible:
            check = hashlib.md5(index.encode()).hexdigest()
            if os.path.exists(os.path.join("_INDEX", check)):
                with open(os.path.join("_INDEX", check)) as f:
                    return json.load(f)
    return []

