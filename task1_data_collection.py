import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


# CONFIGURATION
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

MAX_STORY_IDS = 500
MAX_STORIES_PER_CATEGORY = 25
MIN_TOTAL_STORIES = 100

DATA_DIR = Path("data")

REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.05

# CATEGORY KEYWORDS
CATEGORY_KEYWORDS = {

    "technology": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "large language model",
        "generative ai",
        "chatgpt",
        "openai",
        "anthropic",
        "gemini",
        "claude",
        "deepseek",
        "qwen",

        "software",
        "computer",
        "computing",
        "programming",
        "programmer",
        "developer",
        "development",
        "coding",
        "code",

        "chip",
        "chips",
        "semiconductor",
        "processor",
        "cpu",
        "gpu",
        "hardware",

        "cloud",
        "database",
        "python",
        "javascript",
        "typescript",
        "rust",
        "java",
        "linux",

        "github",
        "git",
        "open source",
        "opensource",

        "robot",
        "robotics",
        "cybersecurity",
        "encryption",

        "technology",
        "tech",
        "internet",
        "web",
        "browser",
        "server",
        "api",
        "startup",

        "application",
        "iphone",
        "android",
        "apple",
        "microsoft",
        "google",
        "meta",
        "amazon",
        "tesla",

        "docker",
        "kubernetes",
        "wasm",
        "webassembly",
        "freebsd",
        "netbsd",
        "postgresql",
        "ruby",
        "emacs",
        "tailscale",
        "proxmox",
        "terraform",
        "three.js",
        "vllm",
        "webgpu",
        "hypervisor",
        "firmware",
        "asic",
    ],

    "worldnews": [
        "election",
        "elections",
        "government",
        "president",
        "presidential",
        "prime minister",
        "minister",

        "politics",
        "political",
        "policy",
        "policies",

        "war",
        "conflict",
        "military",
        "army",

        "country",
        "countries",

        "parliament",
        "congress",
        "senate",
        "geopolitics",
        "diplomacy",
        "diplomatic",

        "sanction",
        "sanctions",

        "protest",
        "protests",

        "democracy",
        "republic",

        "nato",
        "united nations",

        "ukraine",
        "russia",
        "china",
        "india",
        "israel",
        "iran",
        "palestine",
        "gaza",

        "usa",
        "united states",

        "europe",
        "european union",

        "uk",
        "britain",
        "france",
        "germany",
        "japan",
        "korea",
        "taiwan",
        "australia",
        "canada",

        "law",
        "laws",
        "legislation",
        "court",
        "courts",
        "lawsuit",
        "supreme court",

        "economy",
        "economic",
        "economics",
        "economist",
        "inflation",

        "tariff",
        "tariffs",
        "trade",
        "imports",
        "import",
        "exports",
        "export",

        "immigration",
        "immigrant",
        "ice",
        "dhs",
        "doj",

        "mayor",
        "governor",
        "senator",
        "representative",

        "federal",
        "state",

        "rights",
        "civil rights",
        "public policy",

        "union",
        "unions",
        "labor",
        "workers",
        "worker",
    ],

    "sports": [
        "football",
        "soccer",
        "cricket",
        "tennis",
        "basketball",
        "baseball",
        "rugby",
        "golf",
        "hockey",
        "volleyball",
        "badminton",

        "boxing",
        "wrestling",
        "cycling",
        "swimming",
        "athletics",
        "marathon",

        "olympics",
        "olympic",

        "fifa",
        "nfl",
        "nba",
        "mlb",
        "nhl",

        "formula 1",
        "formula one",
        "f1",
        "motorsport",
        "racing",

        "athlete",
        "athletes",

        "championship",
        "championships",

        "league",
        "tournament",
        "tournaments",

        "world cup",
        "premier league",

        "sports",
        "sport",

        "player",
        "players",

        "team",
        "teams",

        "coach",
        "coaching",

        "match",
        "matches",
    ],

    "science": [
        "science",
        "scientist",
        "scientists",

        "research",
        "researcher",
        "researchers",

        "study",
        "studies",

        "nasa",
        "space",

        "physics",
        "physicist",

        "biology",
        "biologist",
        "biological",

        "chemistry",
        "chemical",

        "astronomy",
        "astronomer",
        "astronomical",

        "climate",
        "climate change",

        "environment",
        "environmental",

        "genetics",
        "genetic",
        "genome",
        "genomic",
        "dna",

        "quantum",
        "experiment",
        "experiments",

        "discovery",
        "discoveries",

        "telescope",

        "planet",
        "planets",
        "mars",
        "moon",
        "moons",

        "earth",
        "ocean",
        "oceans",

        "universe",
        "galaxy",
        "galaxies",

        "star",
        "stars",
        "solar",

        "medicine",
        "medical",
        "vaccine",
        "vaccines",

        "disease",
        "diseases",

        "evolution",
        "neuroscience",
        "brain",

        "laboratory",
        "lab",

        "fossil",
        "fossils",
        "paleontology",

        "archaeology",
        "archaeological",

        "nature",
        "biodiversity",
        "ecosystem",
        "ecosystems",

        "octopus",
        "animal",
        "animals",

        "seismic",
        "earthquake",
        "geology",
        "geological",

        "mathematics",
        "mathematical",
        "math",
        "mathematician",

        "theorem",
        "theorems",
        "proof",
        "proofs",

        "navier stokes",
        "navier-stokes",

        "fermat",
        "geometry",
        "geometric",

        "physical",

        "water",
        "sleep",
        "pollution",
    ],

    "entertainment": [
        "movie",
        "movies",
        "film",
        "films",

        "music",
        "musician",

        "actor",
        "actors",
        "actress",

        "celebrity",
        "celebrities",

        "television",
        "tv",
        "series",

        "show",
        "shows",

        "netflix",
        "hollywood",
        "streaming",

        "album",
        "albums",

        "song",
        "songs",

        "singer",
        "director",
        "cinema",

        "entertainment",

        "comedy",
        "comedian",

        "podcast",
        "podcasts",

        "youtube",
        "twitch",
        "spotify",

        "concert",
        "concerts",

        "festival",

        "theater",
        "theatre",

        "book",
        "books",

        "novel",
        "novels",
        "author",

        "gaming",
        "video game",
        "video games",

        "game",
        "games",
    ],
}


# NORMALIZE TEXT
def normalize_text(text):
    text = str(text).lower()

    text = text.replace("-", " ")

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# CHECK KEYWORD
def keyword_matches(text, keyword):
    keyword = normalize_text(keyword)

    pattern = rf"\b{re.escape(keyword)}\b"

    return re.search(pattern, text) is not None


# CLASSIFY STORY
def get_category(title):
    normalized_title = normalize_text(title)

    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword_matches(
                normalized_title,
                keyword
            ):
                score += 1

        category_scores[category] = score

    best_category = max(
        category_scores,
        key=category_scores.get
    )

    best_score = category_scores[best_category]

    if best_score == 0:
        return None

    return best_category


# FETCH TOP STORY IDS
def fetch_top_story_ids():

    response = requests.get(
        TOP_STORIES_URL,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    story_ids = response.json()

    if not isinstance(story_ids, list):
        raise ValueError(
            "Unexpected Hacker News API response."
        )

    return story_ids[:MAX_STORY_IDS]


# FETCH STORY
def fetch_story(story_id):

    try:

        response = requests.get(
            ITEM_URL.format(story_id),
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        story = response.json()

        if not isinstance(story, dict):
            return None

        return story

    except requests.RequestException as error:

        print(
            f"Request failed for story "
            f"{story_id}: {error}"
        )

        return None

    except ValueError:

        print(
            f"Invalid JSON for story "
            f"{story_id}"
        )

        return None


# BUILD REQUIRED RECORD
def build_story_record(story, category):

    return {
        "post_id": story.get("id"),

        "title": str(
            story.get("title", "")
        ).strip(),

        "category": category,

        "score": story.get(
            "score",
            0
        ),

        "num_comments": story.get(
            "descendants",
            0
        ),

        "author": story.get("by"),

        "collected_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# SAVE JSON
def save_json(stories):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    date_string = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d")

    output_path = (
        DATA_DIR
        / f"trends_{date_string}.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            stories,
            file,
            indent=4,
            ensure_ascii=False
        )

    return output_path


# MAIN
def main():

    print("=" * 70)
    print("TrendPulse - Task 1: Data Collection")
    print("=" * 70)

    # FETCH TOP STORIES
    print("\nFetching Hacker News top stories...")

    try:

        story_ids = fetch_top_story_ids()

    except requests.RequestException as error:

        print("\nERROR: Unable to connect to Hacker News API.")
        print(error)

        return

    except ValueError as error:

        print("\nERROR: Invalid API response.")
        print(error)

        return

    print(
        f"Received {len(story_ids)} story IDs."
    )

    print(
        f"Processing first {MAX_STORY_IDS} stories...\n"
    )

    # STORAGE
    collected_stories = []

    processed_ids = set()

    category_counts = {
        category: 0
        for category in CATEGORY_KEYWORDS
    }

    # PROCESS STORIES
    for index, story_id in enumerate(
        story_ids,
        start=1
    ):

        # Stop once every category reaches 25.
        if all(
            count >= MAX_STORIES_PER_CATEGORY
            for count in category_counts.values()
        ):
            break

        # Avoid duplicate IDs.
        if story_id in processed_ids:
            continue

        processed_ids.add(story_id)

        story = fetch_story(story_id)

        if story is None:
            continue

        # Only process Hacker News stories.
        if story.get("type") != "story":
            continue

        title = story.get("title")

        if not title:
            continue

        # CLASSIFY
        category = get_category(title)

        # If no category matches,
        # simply skip the story.
        # Nothing is saved anywhere.
        if category is None:
            continue

        # CATEGORY LIMIT

        if (
            category_counts[category]
            >= MAX_STORIES_PER_CATEGORY
        ):
            continue

        # CREATE RECORD
        record = build_story_record(
            story,
            category
        )

        collected_stories.append(record)

        category_counts[category] += 1

        print(
            f"[{index:03d}/500] "
            f"{category:<15} "
            f"{record['title'][:75]}"
        )

        time.sleep(REQUEST_DELAY)

    # SUMMARY
    print("\n" + "=" * 70)
    print("COLLECTION SUMMARY")
    print("=" * 70)

    print(
        f"Total stories collected: "
        f"{len(collected_stories)}"
    )

    print("\nStories by category:")

    for category, count in category_counts.items():

        print(
            f"  {category:<15}: {count}"
        )

    # VALIDATION
    if len(collected_stories) < MIN_TOTAL_STORIES:

        print("\n" + "=" * 70)
        print("COLLECTION INCOMPLETE")
        print("=" * 70)

        print(
            f"Collected only "
            f"{len(collected_stories)} stories."
        )

        print(
            f"Minimum required: "
            f"{MIN_TOTAL_STORIES}"
        )

        print(
            "\nTask 1 JSON was NOT saved "
            "because the minimum requirement "
            "was not reached."
        )

        return

    # SAVE JSON
    output_path = save_json(
        collected_stories
    )

    print("\n" + "=" * 70)
    print("TASK 1 COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Total stories: "
        f"{len(collected_stories)}"
    )

    print(
        f"JSON saved to: "
        f"{output_path}"
    )

    print("=" * 70)


# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()