from pathlib import Path

from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    RANKING_STRATEGIES,
    recommend_songs,
    score_song,
)


def test_load_songs_reads_csv_and_converts_numeric_fields():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"

    songs = load_songs(str(csv_path))

    assert len(songs) == 18
    assert songs[0]["title"] == "Sunrise City"
    assert songs[0]["id"] == 1
    assert isinstance(songs[0]["tempo_bpm"], int)
    assert isinstance(songs[0]["popularity"], int)
    assert isinstance(songs[0]["release_decade"], int)
    assert songs[0]["mood_tags"] == ["uplifting", "bright"]
    for field in ("energy", "valence", "danceability", "acousticness"):
        assert isinstance(songs[0][field], float)
    assert all(0 <= song["popularity"] <= 100 for song in songs)
    assert all(song["release_decade"] % 10 == 0 for song in songs)
    assert all(song["mood_tags"] and song["vocal_style"] and song["lyrical_theme"] for song in songs)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
            popularity=88,
            release_decade=2020,
            mood_tags=["uplifting", "bright"],
            vocal_style="group",
            lyrical_theme="new beginnings",
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
            popularity=54,
            release_decade=2020,
            mood_tags=["calm", "reflective"],
            vocal_style="solo",
            lyrical_theme="study",
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_popularity=80,
        preferred_decade=2020,
        preferred_mood_tags=["uplifting"],
        preferred_vocal_style="group",
        preferred_lyrical_theme="new beginnings",
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_popularity=80,
        preferred_decade=2020,
        preferred_mood_tags=["uplifting"],
        preferred_vocal_style="group",
        preferred_lyrical_theme="new beginnings",
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_applies_genre_mood_and_energy_weights():
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.8,
        "target_popularity": 100,
        "preferred_decade": 2010,
        "preferred_mood_tags": ["driven"],
        "preferred_vocal_style": "group",
        "preferred_lyrical_theme": "effort",
        "likes_acoustic": False,
    }
    song = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.5,
        "popularity": 70,
        "release_decade": 2010,
        "mood_tags": ["driven", "focused"],
        "vocal_style": "group",
        "lyrical_theme": "effort",
        "acousticness": 0.2,
    }

    score, reasons = score_song(user_prefs, song)

    assert score == 6.6
    assert reasons == [
        "+1.0 genre match: rock",
        "+1.0 mood match: intense",
        "+1.40 energy similarity (2x weight)",
        "+0.70 popularity similarity",
        "+0.5 release decade match: 2010s",
        "+0.5 detailed mood match: driven",
        "+0.5 vocal style match: group",
        "+0.5 lyrical theme match: effort",
        "+0.5 acoustic preference match",
    ]


def test_score_song_uses_only_energy_similarity_when_genre_and_mood_differ():
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.8,
        "target_popularity": 100,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["uplifting"],
        "preferred_vocal_style": "solo",
        "preferred_lyrical_theme": "achievement",
        "likes_acoustic": True,
    }
    song = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.8,
        "popularity": 0,
        "release_decade": 2010,
        "mood_tags": ["calm"],
        "vocal_style": "group",
        "lyrical_theme": "study",
        "acousticness": 0.2,
    }

    score, reasons = score_song(user_prefs, song)

    assert score == 2.0
    assert reasons == [
        "+2.00 energy similarity (2x weight)",
        "+0.00 popularity similarity",
    ]


def test_score_song_maximum_is_seven_point_five():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_popularity": 80,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["uplifting"],
        "preferred_vocal_style": "group",
        "preferred_lyrical_theme": "new beginnings",
        "likes_acoustic": False,
    }
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "popularity": 80,
        "release_decade": 2020,
        "mood_tags": ["uplifting"],
        "vocal_style": "group",
        "lyrical_theme": "new beginnings",
        "acousticness": 0.2,
    }

    score, _ = score_song(user_prefs, song)

    assert score == 7.5


def test_recommend_songs_ranks_all_songs_and_returns_top_k_with_reasons():
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.8,
        "target_popularity": 50,
        "preferred_decade": 2010,
        "preferred_mood_tags": [],
        "preferred_vocal_style": "instrumental",
        "preferred_lyrical_theme": "concentration",
        "likes_acoustic": True,
    }

    def song(title, genre, mood, energy, artist):
        return {
            "title": title,
            "artist": artist,
            "genre": genre,
            "mood": mood,
            "energy": energy,
            "popularity": 50,
            "release_decade": 2010,
            "mood_tags": [],
            "vocal_style": "instrumental",
            "lyrical_theme": "concentration",
            "acousticness": 0.9,
        }

    songs = [
        song("Chill Track", "lofi", "chill", 0.8, "LoRoom"),
        song("Rock Track", "rock", "intense", 0.5, "Rock Band"),
        song("Happy Rock", "rock", "happy", 0.8, "Other Rock Band"),
    ]

    recommendations = recommend_songs(user_prefs, songs, k=2)

    assert [song["title"] for song, _, _ in recommendations] == [
        "Rock Track",
        "Happy Rock",
    ]
    assert recommendations[0][1] == 6.4
    assert "genre match" in recommendations[0][2]
    assert len(recommend_songs(user_prefs, songs, k=0)) == 0


def test_recommend_songs_penalizes_repeated_artists_and_explains_penalty():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_popularity": 80,
        "preferred_decade": 2020,
        "preferred_mood_tags": ["uplifting"],
        "preferred_vocal_style": "group",
        "preferred_lyrical_theme": "new beginnings",
        "likes_acoustic": False,
    }
    matching_song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "popularity": 80,
        "release_decade": 2020,
        "mood_tags": ["uplifting"],
        "vocal_style": "group",
        "lyrical_theme": "new beginnings",
        "acousticness": 0.2,
    }
    songs = [
        {**matching_song, "title": "First Track", "artist": "Same Artist"},
        {**matching_song, "title": "Second Track", "artist": "Same Artist"},
        {**matching_song, "title": "Different Artist Track", "artist": "Another Artist"},
    ]

    recommendations = recommend_songs(user_prefs, songs, k=3)

    assert [song["title"] for song, _, _ in recommendations] == [
        "First Track",
        "Different Artist Track",
        "Second Track",
    ]
    assert recommendations[0][1] == 7.5
    assert recommendations[1][1] == 7.5
    assert recommendations[2][1] == 6.5
    assert "-1.0 repeat-artist penalty: Same Artist" in recommendations[2][2]


def test_ranking_strategies_emphasize_their_preferred_feature():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_popularity": 50,
        "preferred_decade": 2010,
        "preferred_mood_tags": [],
        "preferred_vocal_style": "instrumental",
        "preferred_lyrical_theme": "focus",
        "likes_acoustic": False,
    }

    def song(title, artist, genre, mood):
        return {
            "title": title,
            "artist": artist,
            "genre": genre,
            "mood": mood,
            "energy": 0.8,
            "popularity": 50,
            "release_decade": 2010,
            "mood_tags": [],
            "vocal_style": "instrumental",
            "lyrical_theme": "focus",
            "acousticness": 0.2,
        }

    songs = [
        song("Mood Match", "Mood Artist", "rock", "happy"),
        song("Genre Match", "Genre Artist", "pop", "sad"),
    ]
    genre_first = recommend_songs(
        user_prefs, songs, k=1, strategy=RANKING_STRATEGIES["Genre-First"]
    )
    mood_first = recommend_songs(
        user_prefs, songs, k=1, strategy=RANKING_STRATEGIES["Mood-First"]
    )

    assert genre_first[0][0]["title"] == "Genre Match"
    assert "genre-first ranking bonus" in genre_first[0][2]
    assert mood_first[0][0]["title"] == "Mood Match"
    assert "mood-first ranking bonus" in mood_first[0][2]
