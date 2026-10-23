from typing import List, Dict, Tuple, Protocol, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int
    release_decade: int
    mood_tags: List[str]
    vocal_style: str
    lyrical_theme: str

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_popularity: int
    preferred_decade: int
    preferred_mood_tags: List[str]
    preferred_vocal_style: str
    preferred_lyrical_theme: str

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song records from a CSV file and convert numeric fields."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = list(csv.DictReader(csv_file))

    integer_fields = {"id", "tempo_bpm", "popularity", "release_decade"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    for song in songs:
        for field in integer_fields:
            song[field] = int(song[field])
        for field in float_fields:
            song[field] = float(song[field])
        song["mood_tags"] = song["mood_tags"].split("|")

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append(f"+1.0 genre match: {song['genre']}")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"+1.0 mood match: {song['mood']}")

    energy_similarity = max(
        0.0, 2.0 * (1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    )
    score += energy_similarity
    reasons.append(f"+{energy_similarity:.2f} energy similarity (2x weight)")

    popularity_similarity = max(
        0.0,
        1.0 - abs(song["popularity"] - user_prefs["target_popularity"]) / 100.0,
    )
    score += popularity_similarity
    reasons.append(f"+{popularity_similarity:.2f} popularity similarity")

    if song["release_decade"] == user_prefs["preferred_decade"]:
        score += 0.5
        reasons.append(f"+0.5 release decade match: {song['release_decade']}s")

    shared_mood_tags = set(song["mood_tags"]) & set(user_prefs["preferred_mood_tags"])
    if shared_mood_tags:
        score += 0.5
        reasons.append(f"+0.5 detailed mood match: {', '.join(sorted(shared_mood_tags))}")

    if song["vocal_style"] == user_prefs["preferred_vocal_style"]:
        score += 0.5
        reasons.append(f"+0.5 vocal style match: {song['vocal_style']}")

    if song["lyrical_theme"] == user_prefs["preferred_lyrical_theme"]:
        score += 0.5
        reasons.append(f"+0.5 lyrical theme match: {song['lyrical_theme']}")

    acoustic_match = (
        song["acousticness"] >= 0.6
        if user_prefs["likes_acoustic"]
        else song["acousticness"] <= 0.4
    )
    if acoustic_match:
        score += 0.5
        reasons.append("+0.5 acoustic preference match")

    return score, reasons


class RankingStrategy(Protocol):
    """Define the scoring interface used to rank songs."""

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        """Score a song and return its reasons."""


class BalancedStrategy:
    """Rank using the full preference score without extra emphasis."""

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        return score_song(user_prefs, song)


class GenreFirstStrategy:
    """Give an additional ranking bonus to a preferred-genre match."""

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score, reasons = score_song(user_prefs, song)
        if song["genre"] == user_prefs["favorite_genre"]:
            score += 2.0
            reasons.append(f"+2.0 genre-first ranking bonus: {song['genre']}")
        return score, reasons


class MoodFirstStrategy:
    """Give an additional ranking bonus to a preferred-mood match."""

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score, reasons = score_song(user_prefs, song)
        if song["mood"] == user_prefs["favorite_mood"]:
            score += 2.0
            reasons.append(f"+2.0 mood-first ranking bonus: {song['mood']}")
        return score, reasons


RANKING_STRATEGIES = {
    "Balanced": BalancedStrategy(),
    "Genre-First": GenreFirstStrategy(),
    "Mood-First": MoodFirstStrategy(),
}


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: Optional[RankingStrategy] = None,
) -> List[Tuple[Dict, float, str]]:
    """Return top songs while reducing repeated-artist recommendations."""
    if strategy is None:
        strategy = RANKING_STRATEGIES["Balanced"]

    remaining = []
    for song in songs:
        score, reasons = strategy.score(user_prefs, song)
        remaining.append((song, score, reasons))

    recommendations = []
    artist_counts = {}
    for _ in range(min(max(0, k), len(remaining))):
        best_index = max(
            range(len(remaining)),
            key=lambda index: remaining[index][1]
            - artist_counts.get(remaining[index][0]["artist"], 0),
        )
        song, base_score, reasons = remaining.pop(best_index)
        repeat_count = artist_counts.get(song["artist"], 0)
        score = base_score - repeat_count
        if repeat_count:
            reasons.append(f"-{repeat_count:.1f} repeat-artist penalty: {song['artist']}")
        artist_counts[song["artist"]] = repeat_count + 1
        recommendations.append((song, score, "; ".join(reasons)))

    return recommendations
