import re
import json
import wikidata_query

def tag_remover(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)



#work in progress, not functional
f = open("nfbc.txt",'r')
xs = f.read().encode().decode('utf-8').split('<b>')
data = []

for i in range(1,4):#x in xs:
    x = xs[i]
    text = tag_remover(x)
    words = re.findall(r'\S+', text)

    y = {
        "text": text,
        "qid": wikidata_query.get_qid(words[0])
    }

    data.append(y)

f = open("json_dump.json",'w')
f.write(json.dumps(data))

    



