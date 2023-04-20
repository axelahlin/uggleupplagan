import re
import json
import wikidata_query
from kbbert import is_LOC


def tag_remover(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data).replace("\n", " ")


def first_sentence(text):
    # todo implement
    pass


def first_chars(text, n):
    return text[:n]


FIRST_ONLY = True

# work in progress, not functional
f = open("../nf.txt", 'r')
xs = f.read().encode().decode('utf-8').split('<b>')
data = []

i = 0

for x in xs:  # x in xs:

    text = tag_remover(x)
    # sentence = first_sentence(text)
    sentence = first_chars(text, 100)

    is_loc, first_word = is_LOC(sentence)
    if not is_loc:
        continue

    qid = wikidata_query.get_qid(first_word)
    y = {
        "text": text,
        "qid": qid
    }

    data.append(y)

    i += 1
    if i % 100 == 0:
        print("iteration: " + str(i))

with open("json_dump.json", 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
