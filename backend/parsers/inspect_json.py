import json

INPUT_FILE = "backend/data/timeline.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

print(type(data))

if isinstance(data, dict):
    print("\nTOP LEVEL KEYS:")
    for key in data.keys():
        print("-", key)

elif isinstance(data, list):
    print("\nLIST LENGTH:")
    print(len(data))

    print("\nFIRST ITEM:")
    print(data[0])