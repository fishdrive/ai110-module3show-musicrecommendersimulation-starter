"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import RANKING_STRATEGIES, load_songs, recommend_songs

RANKING_MODE = "Balanced"

USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
        "target_popularity": 80,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["uplifting", "bright"],
        "preferred_vocal_style": "group",
        "preferred_lyrical_theme": "new beginnings",
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_popularity": 55,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["calm", "reflective"],
        "preferred_vocal_style": "solo",
        "preferred_lyrical_theme": "study",
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
        "target_popularity": 75,
        "preferred_decade": 2010,
        "preferred_mood_tags": ["determined", "intense"],
        "preferred_vocal_style": "group",
        "preferred_lyrical_theme": "perseverance",
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    user_prefs = USER_PROFILES["High-Energy Pop"]

    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=5,
        strategy=RANKING_STRATEGIES[RANKING_MODE],
    )

    print(f"\nTop recommendations ({RANKING_MODE}):")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")


if __name__ == "__main__":
    main()
