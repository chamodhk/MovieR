from gliner import GLiNER

# Initialize GLiNER with the base model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Sample text for entity prediction
text = """
Interstellar was a really great film in my opinion, there are a few things i didnt like but all in all it moved with a pretty good flow and all the space moments were so tense it made my heart flutter and stop throughout. The music, the dire situations and setbacks. The humanity and struggle of it all, perfect. Ive heard some remark the 4th dimension moments were off the wall and perhaps they are right, but how else would you depict a 4th dimension in 3 dimensions accurately or more believably?

Anyways i just want to know what other movies are on par with interstellar. Id consider the following as all top tier movies: gattica, pulp fiction, v for vendetta, gladiator, the lord of the rings trilogy, true grit (jeff bridges), the matrix trilogy. However none of these gives me the same tense anxiety and holds me to the edge of my seat like interstellar.
"""

# Labels for entity prediction
# Most GLiNER models should work best when entity types are in lower case or title case
labels = ["Movie", "TV Series"]

# Perform entity prediction
entities = model.predict_entities(text, labels, threshold=0.5)

# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])