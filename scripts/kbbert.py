from transformers import pipeline

nlp = pipeline('ner', model='KB/bert-base-swedish-cased-ner',
               tokenizer='KB/bert-base-swedish-cased-ner')

word = []
# word.append('Aalborg är en stad där Niels Mikkelsen Aalborg bor')
# {"text": "Aak [ak], holl., ett slags lastpråm eller flatbottnadt fartyg, som begagnas på Rhen.\n\n"}
word.append('Niels Mikkelsen Aalborg bor i Aalborg')
word.append('Springa, är ett ord som betyder att man springer.')


def ner(sentence):
    l = []

    for token in nlp(sentence):

        if token['word'].startswith('##'):
            if (len(l) == 0):  # special case
                l += [token]
            else:
                l[-1]['word'] += token['word'][2:]
        else:
            l += [token]
    return l


def is_LOC(sentence, pos=0):

    l = ner(sentence)

    if len(l) == 0:
        return False, None

    if not sentence.startswith(l[pos]['word']):
        return False, None

    return (l[pos]['entity'] == 'LOC', l[pos]['word'])
