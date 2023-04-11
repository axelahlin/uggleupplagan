import requests,os

# Define the URL pattern and range of serial letters
url_pattern = "http://runeberg.org/download.pl?mode=ocrtext&work={}"
start_letter = "nfba"
end_letter = "nfcr"

# Loop through the range of serial letters and download the corresponding file
for letter in range(ord(start_letter[-1]), ord(end_letter[-1])+1):
    for prefix in (start_letter[:-1], end_letter[:-1]):
        url = url_pattern.format(prefix+chr(letter))
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            # Save the file to the local disk
            filename = url.split("/")[-1]
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Downloaded", filename)
        else:
            print("Failed to download", url)

# Rename the files to match their serial lettering
for letter in range(ord(start_letter[-1]), ord(end_letter[-1])+1):
    for prefix in (start_letter[:-1], end_letter[:-1]):
        old_filename = "download.pl?mode=ocrtext&work={}".format(prefix+chr(letter))
        new_filename = prefix + chr(letter) + ".txt"
        os.rename(old_filename, new_filename)
        print("Renamed", old_filename, "to", new_filename)

# Merge the files into a single file called "nf.txt"
with open("nf.txt", "w", encoding="utf-8") as outfile:
    for letter in range(ord(start_letter[-1]), ord(end_letter[-1])+1):
        for prefix in (start_letter[:-1], end_letter[:-1]):
            filename = prefix + chr(letter) + ".txt"
            with open(filename, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # Add a newline after each file
            print("Merged", filename)
            if os.path.exists(filename):
                os.remove(filename)
            else:
                print("The file does not exist")
    
print("All files merged into nf.txt")
