import json
import csv
from pathlib import Path
from collections import Counter
from datetime import datetime

RAW_FILE = Path("data/raw/fuel_prices.json")
CLEAN_FILE = Path("data/processed/fuel_prices_clean.csv")


def load_raw_data():
    with open(
        RAW_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_clean_data():
    with open(
        CLEAN_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return list(
            csv.DictReader(file)
        )


def validate_duplicates(clean_data):

    keys = [
        (
            row["date"],
            row["fuel_type"],
            row["region"]
        )
        for row in clean_data
    ]

    counts = Counter(keys)

    duplicates = [
        key
        for key, count in counts.items()
        if count > 1
    ]

    print("\n1. Duplicate records")
    print(
        f"Duplicate keys found: "
        f"{len(duplicates)}"
    )


def validate_missing_prices(clean_data):

    missing = [
        row
        for row in clean_data
        if row["price"] == ""
    ]

    print("\n2. Missing prices")
    print(
        f"Missing price records: "
        f"{len(missing)}"
    )


def validate_dates(clean_data):

    dates = sorted(
        set(
            datetime.strptime(
                row["date"],
                "%Y-%m-%d"
            ).date()
            for row in clean_data
        )
    )

    irregular_intervals = []

    for previous, current in zip(
        dates,
        dates[1:]
    ):

        difference = (
            current - previous
        ).days

        if difference != 7:

            irregular_intervals.append(
                (
                    previous,
                    current,
                    difference
                )
            )

    print("\n3. Date interval validation")

    print(
        f"Unique dates: {len(dates)}"
    )

    print(
        f"Irregular intervals found: "
        f"{len(irregular_intervals)}"
    )

    if irregular_intervals:

        print(
            "First few irregular intervals:"
        )

        for interval in irregular_intervals[:10]:

            print(
                f"- {interval[0]} → "
                f"{interval[1]} "
                f"({interval[2]} days between observations)"
            )


def validate_wow_change(
    raw_data,
    clean_data
):

    source_changes = {}

    for record in raw_data:

        if record.get(
            "series_type"
        ) != "change_weekly":
            continue

        date = record["date"]

        source_changes[
            (date, "RON95", "Malaysia")
        ] = record.get("ron95")

        source_changes[
            (date, "RON97", "Malaysia")
        ] = record.get("ron97")

        source_changes[
            (date, "Diesel", "Peninsular")
        ] = record.get("diesel")

        source_changes[
            (date, "Diesel", "East Malaysia")
        ] = record.get(
            "diesel_eastmsia"
        )

    comparisons = 0
    mismatches = []

    for row in clean_data:

        wow = row["wow_change"]

        # First observation has no previous value
        if wow == "":
            continue

        key = (
            row["date"],
            row["fuel_type"],
            row["region"]
        )

        source_value = source_changes.get(
            key
        )

        if source_value is None:
            continue

        calculated_value = float(wow)

        if abs(
            calculated_value - source_value
        ) > 0.0001:

            mismatches.append(
                (
                    key,
                    calculated_value,
                    source_value
                )
            )

        comparisons += 1

    print("\n4. Week-over-week validation")

    print(
        f"Comparisons made: "
        f"{comparisons}"
    )

    print(
        f"Mismatches found: "
        f"{len(mismatches)}"
    )

    if mismatches:

        print(
            "First few mismatches:"
        )

        for mismatch in mismatches[:10]:
            print(mismatch)


def main():

    print(
        "Starting fuel-price "
        "data quality validation..."
    )

    raw_data = load_raw_data()

    clean_data = load_clean_data()

    print(
        f"\nRaw records: "
        f"{len(raw_data)}"
    )

    print(
        f"Clean records: "
        f"{len(clean_data)}"
    )

    validate_duplicates(
        clean_data
    )

    validate_missing_prices(
        clean_data
    )

    validate_dates(
        clean_data
    )

    validate_wow_change(
        raw_data,
        clean_data
    )

    print(
        "\nValidation completed."
    )


if __name__ == "__main__":
    main()