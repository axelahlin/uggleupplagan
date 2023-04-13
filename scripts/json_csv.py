import json
import csv

#script for writing json to csv

# Load JSON file
with open('200_manual.json', 'r') as f:
    data = json.load(f)

# Open CSV file for writing
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write header row
    writer.writerow(['text', 'qid', 'geographic_loc'])

    # Write data rows
    for item in data:
        writer.writerow([item['text'], item['qid'], item['geographic_loc']])
