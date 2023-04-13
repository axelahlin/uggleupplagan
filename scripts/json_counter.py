import json

#script for keeping track of how many articles that have been annotated


with open('200_manual.json', 'r') as f:
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