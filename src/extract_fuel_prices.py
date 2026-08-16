import requests
import json
from pathlib import Path

API_URL = "https://api.data.gov.my/data-catalogue?id=fuelprice"

OUTPUT_FILE = Path("data/raw/fuel_prices.json")


def extract_fuel_prices():
    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    data = response.json()

    return data


def save_raw_data(data):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print(f"Saved {len(data)} records to {OUTPUT_FILE}")


def main():
    print("Extracting Malaysian fuel price data...")

    data = extract_fuel_prices()

    print(f"Records received: {len(data)}")

    save_raw_data(data)

    print("Extraction completed successfully.")


if __name__ == "__main__":
    main()