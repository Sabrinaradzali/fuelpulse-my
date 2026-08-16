import json
from pathlib import Path
from collections import Counter

INPUT_FILE = Path("data/raw/fuel_prices.json")


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    data = load_data()

    print(f"Total records: {len(data)}")

    # Count each series type
    series_counts = Counter(
        record.get("series_type")
        for record in data
    )

    print("\nSeries type counts:")

    for series_type, count in series_counts.items():
        print(f"- {series_type}: {count}")

    # Show examples of each series type
    print("\nExample records:")

    for series_type in series_counts:
        print(f"\n[{series_type}]")

        examples = [
            record
            for record in data
            if record.get("series_type") == series_type
        ][:3]

        for record in examples:
            print(record)


if __name__ == "__main__":
    main()