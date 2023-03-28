### A scraper custom made for downloading the text from all encyklopedia entries from the Nordisk Familjebok encyclopedia of 1904, available at project gutenberg.com
from urllib.request import urlopen

DELIM_BEGIN = "<!-- mode=normal -->"
DELIM_END = "<!-- NEWIMAGE2 -->"

FILENAME = 'sammanfattning.txt'
ERROR = "-1"

# Example format:
# http://runeberg.org/nfba/0013.html
# http://runeberg.org/nfcd/q0023.html

# for some reason, nfba and nfbb start with 0013 instead of 0017, we will do these manually. 

url_range_b = 'abcdefghijklmnopqrst'
url_range_c = 'abcdefghijklmn'

url_base = "http://runeberg.org/nf" 
suffix = '.html'

OK = "200 OK"

def scrape():

    filename = "b.txt"
    artNo = 13 
    special_url_a = url_base + 'b' + 'b' + '/' + '00' + str(artNo) + suffix
    page = urlopen(special_url_a)
    text = ""
    with open(filename, 'w') as f:
        while (page.status == 200):
            print(artNo)
            html=page.read().decode("utf-8")
            artNo += 1
            if(artNo < 100):
                special_url_a = url_base + 'b' + 'a' + '/' + '00' + str(artNo) + suffix
            else:
                special_url_a = url_base + 'b' + 'a' + '/' + '0' + str(artNo) + suffix

            text = get_text(html)
            f.write(text)
            page = urlopen(special_url_a)


def scrape():

    filename = "master.txt"
    URL = "http://runeberg.org/download.pl?mode=ocrtext&work=nf"
    text = ""
    with open(filename, 'w') as f:
        
        for pre in ('b', 'c'):
            for c in url_range_b:
                url = URL + pre + c
                page = urlopen(url)
                f.write(page.read().decode('utf-8'))
            

def get_url():
    pass

def get_text(html):

    
    start_index = html.find(DELIM_BEGIN)
    end_index = html.find(DELIM_END)

    text= html[start_index:end_index]

    return text


if __name__ == "__main__":
    scrape()