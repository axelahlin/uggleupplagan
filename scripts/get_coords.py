from SPARQLWrapper import SPARQLWrapper, JSON
import requests


def get_coords(qid):
    endpoint_url = "https://query.wikidata.org/sparql"

    # loop through articles if p625 is missing, if none set q0

    query = """
PREFIX  schema: <http://schema.org/>
PREFIX  bd:   <http://www.bigdata.com/rdf#>
PREFIX  wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX  wikibase: <http://wikiba.se/ontology#>

SELECT DISTINCT  (SAMPLE(?DR) AS ?coords)
WHERE
{ ?article  schema:about       ?item ;
    FILTER ( ?item = <http://www.wikidata.org/entity/""" + qid + """> )
    ?item  wdt:P625  ?DR 
    SERVICE wikibase:label
    { bd:serviceParam
                wikibase:language  "sv"
    }
}
    """

    # create a new SPARQLWrapper object and set the query and endpoint URLd
    user_agent = 'NLP project; ax5047ah-s@student.lu.se al5247my-s@student.lu.se)'
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
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
        print(results)
        return None


def get_coords_raw(qid):
    endpoint_url = "https://query.wikidata.org/sparql"

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
        print(results)
        return None
