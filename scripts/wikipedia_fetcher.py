import wikipedia, re

def get_text(query):
    # Set the language of Wikipedia you want to use
    wikipedia.set_lang("sv")

    # Set the title of the Wikipedia page you want to get
    page_title = query#"Älmhult"

    # Get the Wikipedia page object
    page = wikipedia.page(page_title)

    result = wikipedia.summary("India", sentences = 2)

    page_text = re.sub(r'\n', '', page.content)

    return result#page_text
   