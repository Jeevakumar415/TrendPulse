import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# CONFIGURATION

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

INPUT_FILE = DATA_DIR / "trends_analysed.csv"

CHART1_FILE = OUTPUT_DIR / "chart1_top_stories.png"
CHART2_FILE = OUTPUT_DIR / "chart2_categories.png"
CHART3_FILE = OUTPUT_DIR / "chart3_scatter.png"


# LOAD DATA

def load_data(file_path):
    """
    Load the analysed TrendPulse dataset.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


# CHART 1 — TOP 10 STORIES BY SCORE

def create_top_stories_chart(df):
    """
    Create a horizontal bar chart showing
    the top 10 stories by score.
    """

    top_stories = (
        df.sort_values(
            by="score",
            ascending=False
        )
        .head(10)
        .sort_values(
            by="score",
            ascending=True
        )
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        top_stories["title"],
        top_stories["score"]
    )

    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Hacker News Stories by Score")

    plt.tight_layout()

    plt.savefig(
        CHART1_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close()

    print(
        f"Chart 1 saved to: {CHART1_FILE}"
    )


# CHART 2 — STORY COUNT BY CATEGORY
def create_category_chart(df):
    """
    Create a bar chart showing the number
    of stories in each category.
    """

    category_counts = (
        df["category"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        category_counts.index,
        category_counts.values
    )

    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Number of Stories by Category")

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.savefig(
        CHART2_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close()

    print(
        f"Chart 2 saved to: {CHART2_FILE}"
    )


# CHART 3 — SCORE VS COMMENTS

def create_scatter_chart(df):
    """
    Create a scatter plot showing score versus
    number of comments.

    Popular stories are distinguished from
    non-popular stories using the is_popular column.
    """

    plt.figure(figsize=(10, 7))

    popular = df[
        df["is_popular"] == True
    ]

    non_popular = df[
        df["is_popular"] == False
    ]

    plt.scatter(
        non_popular["score"],
        non_popular["num_comments"],
        label="Non-popular",
        alpha=0.7
    )

    plt.scatter(
        popular["score"],
        popular["num_comments"],
        label="Popular",
        alpha=0.7
    )

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title(
        "Story Score vs. Number of Comments"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        CHART3_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close()

    print(
        f"Chart 3 saved to: {CHART3_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("TrendPulse - Task 4: Visualization")
    print("=" * 70)

    # --------------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    print(
        f"\nLoading analysed data from: "
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
        f"Stories loaded: {len(df)}"
    )

    # CHART 1
    print(
        "\nCreating Chart 1..."
    )

    create_top_stories_chart(
        df
    )

    # CHART 2
    print(
        "\nCreating Chart 2..."
    )

    create_category_chart(
        df
    )

    # CHART 3
    print(
        "\nCreating Chart 3..."
    )

    create_scatter_chart(
        df
    )

    # FINAL OUTPUT
    print("\n" + "=" * 70)
    print("TASK 4 COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated visualization files:")

    print(
        f"1. {CHART1_FILE}"
    )

    print(
        f"2. {CHART2_FILE}"
    )

    print(
        f"3. {CHART3_FILE}"
    )

    print("\n" + "=" * 70)
    print("TRENDPULSE PROJECT COMPLETED")
    print("=" * 70)

# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()