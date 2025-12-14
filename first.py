import json
import re
from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

labels = ["Movie", "TV Series"]

BAD_PATTERNS = [
    r"tt\d+",                  # IMDb ID
    r"[A-Za-z]:\\Users",       # file path
    r"^\d+$",                  # numbers
    r"^\w{1,2}$",              # single letters
]


black_list = [
    "movie",
]


def is_bad_pattern(text):
    for pattern in BAD_PATTERNS:
        if re.match(text, pattern):
            return True
        
    return False
        
def filter_enities(entity_set):
    ens = set() 
    for en in entity_set:
        if is_bad_pattern(en["text"].lower()):
            pass 
        else: 
            ens.add(en["text"].title())
    return ens



file_path = "MovieSuggestions_comments"
count = 0
with open(file_path, "r", encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            # print(obj['body'])
            entities = model.predict_entities(obj["body"], labels, threshold=0.5)
            if entities:
                print("\n")
                for entity in filter_enities(entities):
                    print(entity, end=",")
            

            count += 1
            if count == 500:
                break
        except json.JSONDecodeError:
            break

