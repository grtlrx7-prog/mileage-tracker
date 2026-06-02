import json
from pprint import pprint

INPUT_FILE = "backend/data/timeline.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

segments = data.get("semanticSegments", [])

print(f"Total segments: {len(segments)}\n")

# Show first 5 segments
for i, segment in enumerate(segments[:5]):

    print(f"\nSEGMENT {i + 1}")
    print("=" * 50)

    pprint(segment)

    print("\n")