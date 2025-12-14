import json


file_path = "MovieSuggestions_comments"
parents = set()
count = 0
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            parents.add(obj['parent_id'])
            # count += 1
            # if (count % 100000 == 0):
            #     print(count, end="\r")
        except:
            break

# print('\n')
print(len(parents))

with open('parents.txt', 'w+') as f:
    for parent in parents:
        print(parent, file=f, end="\n")
