import re

def tag_remover(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)



