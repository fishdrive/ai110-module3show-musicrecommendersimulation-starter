# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project recommends songs from a small CSV catalog. It compares each
song's features with a listener profile, ranks the results, and explains each
score.

---

## How The System Works

Real-world streaming services such as Spotify and YouTube use signals such as
listening history, skips, saves, and similarities between users, along with
song details and audio features. This project uses a content-based approach.
It compares song features with a listener's preferences, scores each song,
then ranks the results. It does not learn from a large community of listeners.

Each song stores identifying details, genre and mood, and audio features such as
energy, tempo, valence, danceability, and acousticness. It also has five
additional features: popularity (0–100), release decade, detailed mood tags,
vocal style, and lyrical theme. The profile includes a matching preference for
each feature used by the scoring logic.

The example taste profile used by the recommender is:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
    "target_popularity": 80,
    "preferred_decade": 2020,
    "preferred_mood_tags": ["uplifting", "bright"],
    "preferred_vocal_style": "group",
    "preferred_lyrical_theme": "new beginnings",
}
```

The current algorithm gives each song a score starting at 0:

- Add **1.0 point** for an exact genre match and **1.0 point** for an exact
  mood match.
- Add up to **2.0 points** for energy closeness. Closer energy earns more.
- Add up to **1.0 point** for popularity closeness on the 0–100 scale.
- Add **0.5 point** each for a release-decade match, any shared detailed mood
  tag, a vocal-style match, and a lyrical-theme match.
- Add **0.5 point** when acousticness fits the acoustic preference: at least
  0.6 for acoustic listeners or at most 0.4 for listeners who prefer less
  acoustic sound.

Popularity closeness is calculated as `max(0, 1 - abs(song_popularity -
target_popularity) / 100)`. Energy closeness is
`2 * max(0, 1 - abs(song_energy - target_energy))`. Songs are ranked by their
total feature score. The maximum feature score is **7.5 points**. During
ranking, each previously selected song by the same artist adds a **1-point
penalty**. This helps avoid filling the list with one artist. The explanation
shows the penalty when it applies.

### Ranking Modes

The recommender uses the Strategy design pattern for ranking modes. Choose a
mode by changing `RANKING_MODE` in `src/main.py`:

```python
RANKING_MODE = "Genre-First"
```

Available modes are **Balanced**, **Genre-First**, and **Mood-First**. Balanced
uses the feature score as-is. Genre-First adds a 2-point bonus for a favorite
genre match. Mood-First adds a 2-point bonus for a favorite mood match. These
bonuses affect the displayed score, and their reasons are shown with the
recommendation. Artist variety is still applied while selecting the top list.
For the High-Energy Pop profile, Balanced ranks “Rooftop Lights” above “Gym
Hero,” while Genre-First moves “Gym Hero” above “Rooftop Lights.” Mood-First
adds its bonus to happy songs.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 18

Top recommendations (Balanced):

1. Sunrise City
   Score: 7.38
   Reasons: +1.0 genre match: pop; +1.0 mood match: happy; +1.96 energy similarity (2x weight); +0.92 popularity similarity; +0.5 release decade match: 2020s; +0.5 detailed mood match: bright, uplifting; +0.5 vocal style match: group; +0.5 lyrical theme match: new beginnings; +0.5 acoustic preference match

2. Rooftop Lights
   Score: 5.85
   Reasons: +1.0 mood match: happy; +1.92 energy similarity (2x weight); +0.93 popularity similarity; +0.5 release decade match: 2020s; +0.5 detailed mood match: uplifting; +0.5 vocal style match: group; +0.5 acoustic preference match

3. Gym Hero
   Score: 4.72
   Reasons: +1.0 genre match: pop; +1.74 energy similarity (2x weight); +0.98 popularity similarity; +0.5 release decade match: 2020s; +0.5 acoustic preference match

4. Afterglow Circuit
   Score: 4.31
   Reasons: +1.82 energy similarity (2x weight); +0.99 popularity similarity; +0.5 release decade match: 2020s; +0.5 vocal style match: group; +0.5 acoustic preference match

5. Island Signal
   Score: 4.19
   Reasons: +1.78 energy similarity (2x weight); +0.91 popularity similarity; +0.5 release decade match: 2020s; +0.5 vocal style match: group; +0.5 acoustic preference match
```

### Results for Named User Profiles

**High-Energy Pop**

```text
Loaded songs: 18
Top recommendations (Balanced):

1. Sunrise City
   Score: 7.38
   Reasons: +1.0 genre match: pop; +1.0 mood match: happy; +1.96 energy similarity (2x weight); +0.92 popularity similarity; +0.5 release decade match: 2020s; +0.5 detailed mood match: bright, uplifting; +0.5 vocal style match: group; +0.5 lyrical theme match: new beginnings; +0.5 acoustic preference match

2. Rooftop Lights
   Score: 5.85
   Reasons: +1.0 mood match: happy; +1.92 energy similarity (2x weight); +0.93 popularity similarity; +0.5 release decade match: 2020s; +0.5 detailed mood match: uplifting; +0.5 vocal style match: group; +0.5 acoustic preference match

3. Gym Hero
   Score: 4.72
   Reasons: +1.0 genre match: pop; +1.74 energy similarity (2x weight); +0.98 popularity similarity; +0.5 release decade match: 2020s; +0.5 acoustic preference match

4. Afterglow Circuit
   Score: 4.31
   Reasons: +1.82 energy similarity (2x weight); +0.99 popularity similarity; +0.5 release decade match: 2020s; +0.5 vocal style match: group; +0.5 acoustic preference match

5. Island Signal
   Score: 4.19
   Reasons: +1.78 energy similarity (2x weight); +0.91 popularity similarity; +0.5 release decade match: 2020s; +0.5 vocal style match: group; +0.5 acoustic preference match
```

**Chill Lofi**

```text
Loaded songs: 18
Top recommendations (Balanced):

1. Library Rain
   Score: 7.49
   Reasons: +1.0 genre match: lofi; +1.0 mood match: chill; +2.00 energy similarity (2x weight); +0.99 popularity similarity; +0.5 release decade match: 2020s; +0.5 detailed mood match: calm, reflective; +0.5 vocal style match: solo; +0.5 lyrical theme match: study; +0.5 acoustic preference match

2. Midnight Coding
   Score: 5.80
   Reasons: +1.0 genre match: lofi; +1.0 mood match: chill; +1.86 energy similarity (2x weight); +0.94 popularity similarity; +0.5 detailed mood match: calm; +0.5 acoustic preference match

3. Spacewalk Thoughts
   Score: 4.74
   Reasons: +1.0 mood match: chill; +1.86 energy similarity (2x weight); +0.88 popularity similarity; +0.5 detailed mood match: calm; +0.5 acoustic preference match

4. Coffee Shop Stories
   Score: 4.40
   Reasons: +1.96 energy similarity (2x weight); +0.94 popularity similarity; +0.5 detailed mood match: reflective; +0.5 vocal style match: solo; +0.5 acoustic preference match

5. Blue Ember
   Score: 4.07
   Reasons: +1.66 energy similarity (2x weight); +0.91 popularity similarity; +0.5 detailed mood match: reflective; +0.5 vocal style match: solo; +0.5 acoustic preference match
```

**Deep Intense Rock**

```text
Loaded songs: 18
Top recommendations (Balanced):

1. Storm Runner
   Score: 7.47
   Reasons: +1.0 genre match: rock; +1.0 mood match: intense; +1.98 energy similarity (2x weight); +0.99 popularity similarity; +0.5 release decade match: 2010s; +0.5 detailed mood match: determined, intense; +0.5 vocal style match: group; +0.5 lyrical theme match: perseverance; +0.5 acoustic preference match

2. Velvet Static
   Score: 4.65
   Reasons: +1.88 energy similarity (2x weight); +0.77 popularity similarity; +0.5 release decade match: 2010s; +0.5 detailed mood match: intense; +0.5 vocal style match: group; +0.5 acoustic preference match

3. Gym Hero
   Score: 4.37
   Reasons: +1.0 mood match: intense; +1.94 energy similarity (2x weight); +0.93 popularity similarity; +0.5 acoustic preference match

4. Sunday Parade
   Score: 3.98
   Reasons: +1.66 energy similarity (2x weight); +0.82 popularity similarity; +0.5 release decade match: 2010s; +0.5 vocal style match: group; +0.5 acoustic preference match

5. Afterglow Circuit
   Score: 3.94
   Reasons: +1.98 energy similarity (2x weight); +0.96 popularity similarity; +0.5 vocal style match: group; +0.5 acoustic preference match
```

---

## Experiments You Tried

### Edge-Case Profile Results

Ran the recommender against conflicting, unsupported, out-of-range, and tie-test
profiles. The output below shows the actual top-five recommendations for each
profile.

**Conflicting preferences: high-energy sad rock**

The edge-case output snapshots below are historical. They were collected
before the current weights, additional scored attributes, and artist-variety
penalty were added. Their scores do not represent the current algorithm.

```text
Profile: {'favorite_genre': 'rock', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}
Top recommendations:

1. Storm Runner
   Score: 2.99
   Reasons: +2.0 genre match: rock; +0.99 energy similarity

2. Afterglow Circuit
   Score: 0.99
   Reasons: +0.99 energy similarity

3. Gym Hero
   Score: 0.97
   Reasons: +0.97 energy similarity

4. Velvet Static
   Score: 0.94
   Reasons: +0.94 energy similarity

5. Sunrise City
   Score: 0.92
   Reasons: +0.92 energy similarity
```

**Unsupported genre and mood**

```text
Profile: {'favorite_genre': 'underwater jazz', 'favorite_mood': 'triumphant', 'target_energy': 0.4, 'likes_acoustic': True}
Top recommendations:

1. Focus Flow
   Score: 1.00
   Reasons: +1.00 energy similarity

2. Midnight Coding
   Score: 0.98
   Reasons: +0.98 energy similarity

3. Coffee Shop Stories
   Score: 0.97
   Reasons: +0.97 energy similarity

4. Library Rain
   Score: 0.95
   Reasons: +0.95 energy similarity

5. Paper Moons
   Score: 0.93
   Reasons: +0.93 energy similarity
```

**Energy target above the expected range**

```text
Profile: {'favorite_genre': 'ambient', 'favorite_mood': 'chill', 'target_energy': 1.5, 'likes_acoustic': True}
Top recommendations:

1. Spacewalk Thoughts
   Score: 3.00
   Reasons: +2.0 genre match: ambient; +1.0 mood match: chill; +0.00 energy similarity

2. Midnight Coding
   Score: 1.00
   Reasons: +1.0 mood match: chill; +0.00 energy similarity

3. Library Rain
   Score: 1.00
   Reasons: +1.0 mood match: chill; +0.00 energy similarity

4. Velvet Static
   Score: 0.46
   Reasons: +0.46 energy similarity

5. Gym Hero
   Score: 0.43
   Reasons: +0.43 energy similarity
```

**Energy target below the expected range**

```text
Profile: {'favorite_genre': 'ambient', 'favorite_mood': 'chill', 'target_energy': -0.5, 'likes_acoustic': True}
Top recommendations:

1. Spacewalk Thoughts
   Score: 3.22
   Reasons: +2.0 genre match: ambient; +1.0 mood match: chill; +0.22 energy similarity

2. Library Rain
   Score: 1.15
   Reasons: +1.0 mood match: chill; +0.15 energy similarity

3. Midnight Coding
   Score: 1.08
   Reasons: +1.0 mood match: chill; +0.08 energy similarity

4. Glasshouse Waltz
   Score: 0.19
   Reasons: +0.19 energy similarity

5. Coffee Shop Stories
   Score: 0.13
   Reasons: +0.13 energy similarity
```

**Tie test at energy 0.5**

```text
Profile: {'favorite_genre': 'not-in-catalog', 'favorite_mood': 'not-in-catalog', 'target_energy': 0.5, 'likes_acoustic': False}
Top recommendations:

1. Blue Ember
   Score: 0.98
   Reasons: +0.98 energy similarity

2. Paper Moons
   Score: 0.97
   Reasons: +0.97 energy similarity

3. Golden Hour Road
   Score: 0.92
   Reasons: +0.92 energy similarity

4. Midnight Coding
   Score: 0.92
   Reasons: +0.92 energy similarity

5. Focus Flow
   Score: 0.90
   Reasons: +0.90 energy similarity
```

---

## Limitations and Risks

The catalog is small, and its popularity values are examples rather than real
listening data. Exact tag matching can miss songs with similar moods or themes.
The score also gives energy a strong weight, which can outweigh other matches.
See the [Model Card](model_card.md) for more limits and evaluation notes.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
