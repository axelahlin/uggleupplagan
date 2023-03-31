import spacy
nlp = spacy.load('sv_core_news_lg')

gpe = [] # countries, cities, states
loc = [] # non gpe locations, mountain ranges, bodies of water

nlp.max_length = 5000000
doc = nlp(open('subtitle.txt').read())
for ent in doc.ents:
    print(ent)
    if (ent.label_ == 'GPE'):
        gpe.append(ent.text)
    elif (ent.label_ == 'LOC'):
        loc.append(ent.text)
        print(ent.text)


cities = []
countries = []
other_places = []
import wikipedia
for text in gpe:
    summary = None
    try:
        summary = str(wikipedia.summary(text))
    except:
        print("Not found in wikipedia: " + text)
    
    if summary is not None:
        if ('city' in summary):
            cities.append(text)
        elif ('country' in summary):
            countries.append(text)
        else:
            other_places.append(text)

for text in loc:
    other_places.append(text)