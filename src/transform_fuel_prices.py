import json
import csv
from pathlib import Path

INPUT_FILE = Path("data/raw/fuel_prices.json")
OUTPUT_FILE = Path("data/processed/fuel_prices_clean.csv")


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_data(data):
    transformed = []

    for record in data:

        # Only use actual fuel-price levels
        if record.get("series_type") != "level":
            continue

        date = record["date"]

        fuel_prices = [
            ("RON95", "Malaysia", record.get("ron95")),
            ("RON97", "Malaysia", record.get("ron97")),
            ("Diesel", "Peninsular", record.get("diesel")),
            ("Diesel", "East Malaysia", record.get("diesel_eastmsia")),
        ]

        for fuel_type, region, price in fuel_prices:

            # Skip records where the price is missing
            if price is None:
                continue

            transformed.append({
                "date": date,
                "fuel_type": fuel_type,
                "region": region,
                "price": price
            })

    return transformed


def calculate_weekly_change(data):
    previous_prices = {}

    for record in data:

        key = (
            record["fuel_type"],
            record["region"]
        )

        previous_price = previous_prices.get(key)

        if previous_price is None:

            # First available observation
            record["wow_change"] = None
            record["wow_change_pct"] = None

        else:

            # Absolute week-over-week change
            wow_change = record["price"] - previous_price

            record["wow_change"] = round(
                wow_change,
                4
            )

            # Percentage week-over-week change
            record["wow_change_pct"] = round(
                (wow_change / previous_price) * 100,
                2
            )

        previous_prices[key] = record["price"]


def save_data(data):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "date",
        "fuel_type",
        "region",
        "price",
        "wow_change",
        "wow_change_pct"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(data)

    print(
        f"Saved {len(data)} records to "
        f"{OUTPUT_FILE}"
    )


def main():

    print("Loading raw fuel-price data...")

    data = load_data()

    print(
        f"Raw records: {len(data)}"
    )

    transformed_data = transform_data(data)

    print(
        f"Level records transformed: "
        f"{len(transformed_data)}"
    )

    calculate_weekly_change(
        transformed_data
    )

    save_data(
        transformed_data
    )

    print(
        "Transformation completed successfully."
    )


if __name__ == "__main__":
    main()