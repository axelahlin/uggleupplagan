from SPARQLWrapper import SPARQLWrapper, JSON

def get_coords(qid):
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """
    PREFIX  schema: <http://schema.org/>
    PREFIX  bd:   <http://www.bigdata.com/rdf#>
    PREFIX  wdt:  <http://www.wikidata.org/prop/direct/>
    PREFIX  wikibase: <http://wikiba.se/ontology#>

    SELECT DISTINCT  (SAMPLE(?DR) AS ?coords)
    WHERE
    { ?article  schema:about       ?item ;
                schema:inLanguage  "en" ;
                schema:isPartOf    <https://en.wikipedia.org/>
        FILTER ( ?item = <http://www.wikidata.org/entity/"""+qid+"""> )
        OPTIONAL
        { ?item  wdt:P625  ?DR }
        SERVICE wikibase:label
        { bd:serviceParam
                    wikibase:language  "en"
        }
    }
    """

    # create a new SPARQLWrapper object and set the query and endpoint URL
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
    except Exception as e:
        print("Error:", e)
        exit()

    if results["results"]["bindings"]:
        point = results["results"]["bindings"][0]["coords"]["value"]

        import re
        regex = r"[^\d\s.]"  # match anything that's not a digit or whitespace
        result = [float(x) for x in re.sub(regex, "", point).split(" ")]  # remove everything that matches the regex  
        print("Point:", result)
        return result
    else:
        print("No coordinates found for Q-ID:", qid)
        return None