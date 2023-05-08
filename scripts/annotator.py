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


def nf_to_json(infile="/home/alfredmyrne/kurser/projekt/edan70-project/nf.txt", outfile="json_dict.json"):
    f = open(infile, 'r')
    xs = f.read().encode().decode('utf-8').split('<b>')
    data = []
    i = 0

    for x in xs:  # x in xs:

        text = tag_remover(x)
        # sentence = first_sentence(text)
        sentence = first_chars(text, 100)

        y = {
            "text": sentence,
        }

        data.append(y)

        i += 1
        if i % 100 == 0:
            print("iteration: " + str(i))

    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def annotate(infile="json_dict.json", outfile="annotated.json"):

    n = 0

    with open(outfile, 'w', encoding='utf8') as o:

        with open(infile, 'r', encoding='utf8') as i:

            data = json.load(i)

            res = []

            for entry in data:
                text = entry['text']
                is_loc, first_word = is_LOC(text)

                qid = None
                if is_loc:
                    qid = wikidata_query.get_qid(first_word, text)

                new_entry = {'text': text, "is_loc": is_loc, "qid": qid}
                res.append(new_entry)

                n += 1
                if n % 100 == 0:
                    print("iteration: " + str(n))

            json.dump(res, o, ensure_ascii=False)


if __name__ == "__main__":
    # nf_to_json()
    annotate()
