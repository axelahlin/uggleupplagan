from transformers import pipeline

# nlp = pipeline('ner', model='KB/bert-base-swedish-cased-ner',
#                tokenizer='KB/bert-base-swedish-cased-ner')

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = AutoTokenizer.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl")
model = AutoModelForTokenClassification.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl")
# tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
# model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")

#nlp = pipeline('ner', model=model,
            #   tokenizer=tokenizer)
nlp = pipeline(task='ner', 
               model='saattrupdan/nbailab-base-ner-scandi', 
               aggregation_strategy='first')

def ner(sentence):
    line = []

    for token in nlp(sentence):

        if token['word'].startswith('##'):
            if (len(line) == 0):  # special case
                line += [token]
            else:
                line[-1]['word'] += token['word'][2:]
        else:
            line += [token]
    return line


def get_headword(sentence, pos=0):

    line = ner(sentence)

    if len(line) == 0:
        return ""

    if not sentence.startswith(line[pos]['word']):
        return "<NO ENTITY FOUND>"

    return line[pos]['word'] #(line[pos]['entity_group'] == 'LOC', line[pos]['word'])
