import requests
import json
import math
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

MAX_LEN = 5


def cosine_sim(sentence1, sentence2):

    # Compute embedding for both lists
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return cosine_scores


def get_qid(word, text):
    # Replace the <language> and <word> placeholders with the actual values
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=sv&search={word}"
    response = requests.get(url)

    # Check if the API call was successful
    if response.status_code == 200:
        data = json.loads(response.content)
        if 'search' in data and len(data['search']) > 0:
            max_len = max(len(data['search']), MAX_LEN)

            cosine_sims = []

            for candidate in data['search'][:max_len]:

                cosine_value = -1 * math.inf
                if 'description' in candidate:
                    cosine_value = cosine_sim(candidate['description'], text)
                elif 'text' in candidate:
                    cosine_value = cosine_sim(candidate['text'], text)

                cosine_sims.append((cosine_value, candidate))

                # best_candidate = max(
                #     [d for d in data['search'][:max_len]], key=lambda d: cosine_sim(d['description'], text))

                # TODO: Save description for use in SBERT cosine sim.
            if len(cosine_sims) == 0:
                print(data)
            _, best_candidate = max(cosine_sims, key=lambda k: k[0])
            return best_candidate['id']
        else:
            return None
    else:
        return None
