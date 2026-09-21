import pandas as pd
import numpy as np
from pathlib import Path


# CONFIGURATION
DATA_DIR = Path("data")

INPUT_FILE = DATA_DIR / "trends_clean.csv"
OUTPUT_FILE = DATA_DIR / "trends_analysed.csv"


# LOAD CLEAN DATA
def load_data(file_path):
    """
    Load the cleaned TrendPulse CSV file.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    df = pd.read_csv(
        file_path
    )

    return df


# BASIC DATAFRAME INFORMATION
def display_basic_information(df):
    """
    Display the first five rows and DataFrame shape.
    """

    print("\n" + "=" * 70)
    print("FIRST FIVE ROWS")
    print("=" * 70)

    print(
        df.head()
        .to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("DATAFRAME SHAPE")
    print("=" * 70)

    print(
        f"Rows    : {df.shape[0]}"
    )

    print(
        f"Columns : {df.shape[1]}"
    )

    print(
        f"Shape   : {df.shape}"
    )


# BASIC STATISTICS
def calculate_basic_statistics(df):
    """
    Calculate average score and average comments.
    """

    average_score = df["score"].mean()

    average_comments = (
        df["num_comments"].mean()
    )

    print("\n" + "=" * 70)
    print("BASIC STATISTICS")
    print("=" * 70)

    print(
        f"Average score: "
        f"{average_score:.2f}"
    )

    print(
        f"Average comments: "
        f"{average_comments:.2f}"
    )

    return average_score, average_comments


# ============================================================
# NUMPY SCORE STATISTICS
# ============================================================

def calculate_numpy_statistics(df):
    """
    Calculate score statistics using NumPy.
    """

    scores = df["score"].to_numpy()

    score_mean = np.mean(scores)

    score_median = np.median(scores)

    score_std = np.std(scores)

    score_max = np.max(scores)

    score_min = np.min(scores)

    print("\n" + "=" * 70)
    print("NUMPY SCORE STATISTICS")
    print("=" * 70)

    print(
        f"Mean               : {score_mean:.2f}"
    )

    print(
        f"Median             : {score_median:.2f}"
    )

    print(
        f"Standard deviation : {score_std:.2f}"
    )

    print(
        f"Maximum            : {score_max}"
    )

    print(
        f"Minimum            : {score_min}"
    )

    return (
        score_mean,
        score_median,
        score_std,
        score_max,
        score_min
    )


# CATEGORY WITH MOST STORIES
def find_top_category(df):
    """
    Find the category containing the most stories.
    """

    category_counts = (
        df["category"]
        .value_counts()
    )

    top_category = (
        category_counts
        .idxmax()
    )

    top_category_count = (
        category_counts
        .max()
    )

    print("\n" + "=" * 70)
    print("CATEGORY ANALYSIS")
    print("=" * 70)

    print(
        "Stories by category:"
    )

    print(
        category_counts
        .to_string()
    )

    print(
        f"\nCategory with most stories: "
        f"{top_category}"
    )

    print(
        f"Number of stories: "
        f"{top_category_count}"
    )

    return (
        top_category,
        top_category_count
    )


# STORY WITH MOST COMMENTS
def find_most_commented_story(df):
    """
    Find the story with the highest number of comments.
    """

    max_comments_index = (
        df["num_comments"]
        .idxmax()
    )

    most_commented_story = (
        df.loc[max_comments_index]
    )

    print("\n" + "=" * 70)
    print("MOST COMMENTED STORY")
    print("=" * 70)

    print(
        f"Title    : "
        f"{most_commented_story['title']}"
    )

    print(
        f"Comments : "
        f"{most_commented_story['num_comments']}"
    )

    print(
        f"Score    : "
        f"{most_commented_story['score']}"
    )

    print(
        f"Category : "
        f"{most_commented_story['category']}"
    )

    return most_commented_story


# ENGAGEMENT
def calculate_engagement(df):
    """
    Calculate engagement for every story.

    Formula:
        engagement = num_comments / (score + 1)
    """

    df["engagement"] = (
        df["num_comments"]
        / (df["score"] + 1)
    )

    return df


# POPULAR STORIES
def calculate_popularity(
    df,
    average_score
):
    """
    Mark stories as popular when their score
    is greater than the average score.

    Formula:
        is_popular = score > average_score
    """

    df["is_popular"] = (
        df["score"] > average_score
    )

    return df


# ============================================================
# DISPLAY ENGAGEMENT INFORMATION
# ============================================================

def display_engagement_information(df):
    """
    Display engagement and popularity statistics.
    """

    print("\n" + "=" * 70)
    print("ENGAGEMENT ANALYSIS")
    print("=" * 70)

    print(
        "Engagement formula:"
    )

    print(
        "engagement = "
        "num_comments / (score + 1)"
    )

    print(
        f"\nAverage engagement: "
        f"{df['engagement'].mean():.4f}"
    )

    popular_count = (
        df["is_popular"]
        .sum()
    )

    non_popular_count = (
        (~df["is_popular"])
        .sum()
    )

    print(
        f"Popular stories: "
        f"{popular_count}"
    )

    print(
        f"Non-popular stories: "
        f"{non_popular_count}"
    )

    print(
        "\nTop 5 stories by engagement:"
    )

    top_engagement = (
        df[
            [
                "title",
                "score",
                "num_comments",
                "engagement",
                "is_popular"
            ]
        ]
        .sort_values(
            by="engagement",
            ascending=False
        )
        .head(5)
    )

    print(
        top_engagement
        .to_string(index=False)
    )


# SAVE ANALYSED DATA
def save_data(df, file_path):
    """
    Save the analysed DataFrame as CSV.
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

    print("\n" + "=" * 70)
    print("ANALYSED DATA SAVED")
    print("=" * 70)

    print(
        f"Output file: "
        f"{file_path}"
    )


# MAIN
def main():

    print("=" * 70)
    print("TrendPulse - Task 3: Analysis")
    print("=" * 70)

    # LOAD DATA
    print(
        f"\nLoading cleaned data from: "
        f"{INPUT_FILE}"
    )

    try:

        df = load_data(
            INPUT_FILE
        )

    except FileNotFoundError as error:

        print(
            f"\nERROR: {error}"
        )

        return

    print(
        f"Rows loaded: "
        f"{len(df)}"
    )

    # BASIC DATAFRAME INFORMATION
    display_basic_information(
        df
    )

    # BASIC STATISTICS
    (
        average_score,
        average_comments
    ) = calculate_basic_statistics(
        df
    )

    # NUMPY STATISTICS
    calculate_numpy_statistics(
        df
    )

    # CATEGORY ANALYSIS
    find_top_category(
        df
    )

    # MOST COMMENTED STORY
    find_most_commented_story(
        df
    )

    # ENGAGEMENT
    df = calculate_engagement(
        df
    )

    # POPULARITY
    df = calculate_popularity(
        df,
        average_score
    )

    # DISPLAY ENGAGEMENT RESULTS
    display_engagement_information(
        df
    )

    # SAVE ANALYSED DATA
    save_data(
        df,
        OUTPUT_FILE
    )

    # FINAL OUTPUT
    print("\n" + "=" * 70)
    print("TASK 3 COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Analysed rows: "
        f"{len(df)}"
    )

    print(
        f"Output: "
        f"{OUTPUT_FILE}"
    )

    print("=" * 70)


# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()