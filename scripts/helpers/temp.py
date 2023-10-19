import json

def convert_json(input_file, output_file):
    with open(input_file) as f:
        data = json.load(f)

    converted_data = []
    for item in data:
        converted_item = {
            "text": item["text"],
            "is_loc": 0,
            "qid": "0"
        }
        converted_data.append(converted_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False)

    print(f"Conversion completed. Converted data saved to {output_file}.")
if __name__ == "__main__":
    input_file = "data/nf.json"
    output_file = "data/nf_converted.json"
    convert_json(input_file, output_file)