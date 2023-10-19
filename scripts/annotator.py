import re
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import math
import scripts.helpers.kbbert as kbb
from sentence_transformers import SentenceTransformer, util


def cosine_sim(sentence1, sentence2, model):
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)
    return util.cos_sim(embeddings1, embeddings2)


def point_extract(point):
    regex = r"[^-\d\s.]"  # match anything that's not a digit or whitespace
    # remove everything that matches the regex

    if point.startswith("http"):
        print("URL returned. Point: " + point)
        # This needs to be revised
        return [-91.0, 181.0]  # invalid coords for placeholder

    result = [float(x) for x in re.sub(regex, "", point).split(" ")]

    return result


def get_best_candidate(main, candidates, max_candidates, model):
    max_len = min(len(candidates), max_candidates)
    cosine_sims = []

    for candidate in candidates[:max_len]:
        cosine_value = -1 * math.inf
        try:  # avoid descriptionless items
            candidate_sentence = candidate["itemDescription"]["value"]
            cosine_value = cosine_sim(candidate_sentence, main, model)
            cosine_sims.append((cosine_value, candidate))
        except:
            cosine_sims.append((0, candidate))

    _, best_candidate = max(cosine_sims, key=lambda k: k[0])
    return best_candidate


def get_and_save_coords(config):
    FILENAME_OUT_JSON = config["annotator"]["output_json_file"]
    FILENAME_IN = config["annotator"]["input_file"]
    endpoint_url = config["annotator"]["endpoint_url"]
    user_agent = config["annotator"]["user_agent"]
    MAX_CANDIDATES = config["annotator"]["max_candidates"]
    transformer_model = config["annotator"]["transformer_model"]
    model = SentenceTransformer(transformer_model)
    debug = config["debug"]

    sparql_query = """
                    SELECT ?item ?itemLabel ?itemDescription ?coords WHERE {{
                    SERVICE wikibase:mwapi {{
                        bd:serviceParam wikibase:endpoint "www.wikidata.org";
                        wikibase:api "EntitySearch";
                        mwapi:search "{}";
                        mwapi:language "sv".
                        ?item wikibase:apiOutputItem mwapi:item.
                        ?num wikibase:apiOrdinal true.
                    }}
                    ?item rdfs:label ?itemLabel.
                    FILTER(LANG(?itemLabel) = "sv" || LANG(?itemLabel) = "[AUTO_LANGUAGE]")
                    OPTIONAL {{
                        ?item schema:description ?itemDescription.
                        FILTER(LANG(?itemDescription) = "sv" || LANG(?itemDescription) = "[AUTO_LANGUAGE]")
                    }}
                    ?item wdt:P625 ?coords.
                    }}
                    ORDER BY ASC(?num)
                    LIMIT 20
                    """

    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setReturnFormat(JSON)

    n = 0
    fails = 0
    with open(FILENAME_OUT_JSON, "w", encoding="utf-8") as json_outfile:
        with open(FILENAME_IN, encoding="utf-8") as i:
            json_data = json.load(i)
            xs = []

            for entry in json_data:
                headword = kbb.get_headword(entry["text"])
                if " l. " in headword:  # disambiguation logic
                    headword = headword.split(" l. ")[0]

                query = sparql_query.format(headword)
                sparql.setQuery(query)
                point = [None, None]
                qid = name = ""

                try:
                    results = sparql.query().convert()
                    if results["results"]["bindings"]:
                        candidates = results["results"]["bindings"]

                        # choose best candidate
                        top_candidate = get_best_candidate(
                            entry["text"], 
                            candidates, 
                            MAX_CANDIDATES,
                            model
                        )

                        point = top_candidate["coords"]["value"]
                        qid_url = top_candidate["item"]["value"]

                        # Match the QID
                        match = re.search(r"/Q\d+", qid_url)
                        if match:
                            qid = match.group(0)[
                                1:
                            ]  # Extract the QID without the leading slash
                        else:
                            if debug:
                                print("qid search went wrong...")

                        try:
                            point = point_extract(point)
                        except:
                            point = [None, None]

                        name = top_candidate["itemLabel"]["value"]
                        if debug:
                            print(f"Found ({name} - {qid} - {point}) for {headword}")
                    else:
                        if debug:
                            print(f"Found nothing for {headword} => {entry['text']}")
                        fails += 1

                    new_entry = {
                        "text": entry["text"],
                        "is_loc": entry["is_loc"],
                        "qid": qid,
                        "latitude": point[0],
                        "longitude": point[1],
                    }
                    xs.append(new_entry)
                except Exception as e:
                    print("Query execution exception: ", e)
                    exit()

                n += 1
                if n % 100 == 0:
                    print(n, " iterations", fails, " fails")
                if n % 1000 == 0:
                    with open(f"data/part{n}_nf_coords.json", "w") as s:
                        json.dump(xs, s, ensure_ascii=False)
            json.dump(xs, json_outfile, ensure_ascii=False)

    print(f"{fails=}")
