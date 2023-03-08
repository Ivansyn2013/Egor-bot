import json

data = []

with open('cenz.txt', encoding='utf-8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            data.append(n)

with open('cenz.json', 'w', encoding='utf-8') as j:
    json.dump(data, j)
