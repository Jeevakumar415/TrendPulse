import json
from pathlib import Path

import pandas as pd


# CONFIGURATION
DATA_DIR = Path("data")

INPUT_FILE = DATA_DIR / "trends_20260910.json"
OUTPUT_FILE = DATA_DIR / "trends_clean.csv"


# LOAD JSON DATA
def load_json_data(file_path):
    """
    Load the collected TrendPulse JSON data.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Expected JSON data to be a list of stories."
        )

    return data


# CREATE DATAFRAME
def create_dataframe(data):
    """
    Convert JSON records into a Pandas DataFrame.
    """

    df = pd.DataFrame(data)

    return df


# CLEAN DATA
def clean_data(df):
    """
    Perform all required data-cleaning operations.
    """

    print("\nStarting data cleaning...")

    # Remove duplicate post IDs
    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=["post_id"],
        keep="first"
    )

    duplicates_removed = (
        before_duplicates - len(df)
    )

    print(
        f"Duplicate rows removed: "
        f"{duplicates_removed}"
    )

    # Remove rows missing required fields
    required_columns = [
        "post_id",
        "title",
        "score"
    ]

    before_missing = len(df)

    df = df.dropna(
        subset=required_columns
    )

    missing_removed = (
        before_missing - len(df)
    )

    print(
        f"Rows missing required fields removed: "
        f"{missing_removed}"
    )

    # Convert score to integer
    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    )

    # Convert number of comments to integer
    df["num_comments"] = pd.to_numeric(
        df["num_comments"],
        errors="coerce"
    )

    # Remove rows where numeric conversion failed.
    df = df.dropna(
        subset=[
            "score",
            "num_comments"
        ]
    )

    # Convert to integers.
    df["score"] = df["score"].astype(int)

    df["num_comments"] = (
        df["num_comments"].astype(int)
    )

    # Remove stories with score below 5
    before_score_filter = len(df)

    df = df[
        df["score"] >= 5
    ].copy()

    low_score_removed = (
        before_score_filter - len(df)
    )

    print(
        f"Stories with score < 5 removed: "
        f"{low_score_removed}"
    )

    # Strip whitespace from titles
    df["title"] = (
        df["title"]
        .astype(str)
        .str.strip()
    )

    # Reset index
    df = df.reset_index(
        drop=True
    )

    return df


# SAVE CLEAN DATA
def save_clean_data(df, file_path):
    """
    Save the cleaned DataFrame as CSV.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8"
    )

    print(
        f"\nCleaned data saved to: "
        f"{file_path}"
    )


# PRINT CATEGORY SUMMARY
def print_category_summary(df):
    """
    Print the number of stories in each category.
    """

    print("\n" + "=" * 70)
    print("CATEGORY SUMMARY")
    print("=" * 70)

    category_summary = (
        df["category"]
        .value_counts()
        .sort_index()
    )

    for category, count in (
        category_summary.items()
    ):

        print(
            f"{category:<20} {count}"
        )

    print("=" * 70)


# MAIN
def main():

    print("=" * 70)
    print("TrendPulse - Task 2: Data Processing")
    print("=" * 70)

    # LOAD DATA
    print(
        f"\nLoading data from: "
        f"{INPUT_FILE}"
    )

    try:

        data = load_json_data(
            INPUT_FILE
        )

    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError
    ) as error:

        print(
            f"\nERROR: {error}"
        )

        return

    print(
        f"Stories loaded: "
        f"{len(data)}"
    )

    # CREATE DATAFRAME
    df = create_dataframe(
        data
    )

    print(
        f"Initial DataFrame rows: "
        f"{len(df)}"
    )

    print(
        f"Initial DataFrame columns: "
        f"{len(df.columns)}"
    )

    # CLEAN DATA
    df = clean_data(
        df
    )

    # DISPLAY FINAL INFORMATION
    print("\n" + "=" * 70)
    print("CLEANING RESULTS")
    print("=" * 70)

    print(
        f"Final cleaned row count: "
        f"{len(df)}"
    )

    print(
        f"Final column count: "
        f"{len(df.columns)}"
    )

    print(
        "\nColumns:"
    )

    for column in df.columns:
        print(
            f"  - {column}"
        )

    # CATEGORY SUMMARY
    print_category_summary(
        df
    )

    # SAVE CSV
    save_clean_data(
        df,
        OUTPUT_FILE
    )

    # FINAL MESSAGE
    print("\n" + "=" * 70)
    print("TASK 2 COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Cleaned dataset: "
        f"{OUTPUT_FILE}"
    )

    print(
        f"Rows: {len(df)}"
    )

    print("=" * 70)


# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()