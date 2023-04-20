from SPARQLWrapper import SPARQLWrapper, JSON


def get_coords(qid):
    endpoint_url = "https://query.wikidata.org/sparql"

    print(qid)

    # loop through articles if p625 is missing, if none set q0

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
        ?item  wdt:P625  ?DR 
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

    if "coords" in results["results"]["bindings"][0]:
        point = results["results"]["bindings"][0]["coords"]["value"]

        import re
        regex = r"[^\d\s.]"  # match anything that's not a digit or whitespace
        # remove everything that matches the regex

        if (point.startswith('http')):
            print("URL returned. Point: " + point)
            # This needs to be revised
            return None

        result = [float(x) for x in re.sub(regex, "", point).split(" ")]

        return result
    else:
        print("No coordinates found for Q-ID:", qid)
        return None
