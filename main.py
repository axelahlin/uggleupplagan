import os,subprocess

def main():

    # check if nf.txt exists, else run text_scraper.py
    if os.path.exists("nf.txt"):
        print("Encyclopedia in nf.txt already exists, skipping text_scraper.py")
    else:
        print("Running text_scraper.py to create encyclopedia in nf.txt")
        subprocess.call(["python", "text_scraper.py"])

    # check if model exists, otherwise train by loading (manually) annotated articles and running tf-idf vectorizer for place

    # run annotating tool:
    #       - ask model
    #       - measure sberts cosine sim on wikipedia introduction and decide according to threshold (see Aachen vs Regierungsbezirk Aachen)
    #       - (optional) set q0 and notify user for review

    # for all places, fetch coordinates (P625)

    # lats, lons = ???, ???

    # print map with lats and lons

    print("Done, exiting")

if __name__ == "__main__":
    main()