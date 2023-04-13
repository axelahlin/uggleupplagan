import spacy,os 
nlp = spacy.load('sv_core_news_lg')#sv_core_news_lg')en_core_web_sm

gpe = [] # countries, cities, states
loc = [] # non gpe locations, mountain ranges, bodies of water

nlp.max_length = 5000000

file_path = os.path.abspath('/home/axel/Code/edan70-project/data/geotext.txt')
with open(file_path) as file:
    doc = nlp(file.read())
for ent in doc.ents:
    print(ent.label_)
    if (ent.label_ == 'GPE'):
        gpe.append(ent.text)
    elif (ent.label_ == 'LOC'):
        loc.append(ent.text)
        print(ent.text)


cities = set() #set or list?
countries = set()
other_places = set()
import wikipedia
for text in loc:
    summary = None
    try:
        summary = str(wikipedia.summary(text))[:100]
    except:
        print("Not found in wikipedia: " + text)
    
    if summary is not None:
        if ('city' in summary):
            cities.add(text)
        elif ('country' in summary):
            countries.add(text)
        else:
            other_places.add(text)

for text in loc:
    other_places.add(text)