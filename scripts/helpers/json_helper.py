import json, csv

#script for keeping track of how many articles that have been annotated

def count(file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Initialize a count variable
    count = 0

    # Loop through each object in the JSON data
    for obj in data:
        # Check if the object has a non-empty "text" field
        if 'text' in obj and obj['text'].strip():
            # Increment the count if the "text" field is non-empty
            count += 1

    # Print the count of objects with non-empty "text" fields
    print(f"Number of JSON objects with non-empty 'text' fields: {count}")

def json_to_csv(file):

    # Load JSON file
    with open(file, 'r') as f:
        data = json.load(f)

    # Open CSV file for writing
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # Write header row
        writer.writerow(['text', 'qid', 'geographic_loc'])

        # Write data rows
        for item in data:
            writer.writerow([item['text'], item['qid'], item['geographic_loc']])
