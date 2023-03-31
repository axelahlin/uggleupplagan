import requests
import json

def get_qid(word):
    # Replace the <language> and <word> placeholders with the actual values
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=sv&search={word}"
    response = requests.get(url)

    # Check if the API call was successful
    if response.status_code == 200:
        data = json.loads(response.content)
        if data['search']:
            return data['search'][0]['id']
        else:
            return None
    else:
        return None


    