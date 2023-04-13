import wikipedia, re

def get_text(query):
    wikipedia.set_lang("sv")
    page_title = query#"Älmhult"

    # Get the wiki page object
    page = wikipedia.page(page_title)

    result = wikipedia.summary("India", sentences = 2)

    page_text = re.sub(r'\n', '', page.content)

    return result#page_text
   