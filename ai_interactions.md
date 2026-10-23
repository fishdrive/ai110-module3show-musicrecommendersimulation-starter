# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to add at least five useful song attributes and update the recommender so those attributes affect its scores. I also asked it to document the prompts, code changes, and manual verification.

**Prompts used:**

> Add five or more meaningful song attributes to the dataset, update the scoring logic to use them consistently, and document the agentic workflow in this file. Keep the examples, tests, and explanations in sync with the new data and scoring.
>
> Add an artist-repeat penalty when selecting the top recommendations. Explain the penalty in each affected result, and document how it encourages variety and what fairness limitations remain.
>
> Implement at least two selectable ranking strategies in a modular design.
> Let the user switch modes in main.py, and document the chosen design pattern and how AI helped brainstorm it.

**What did the agent generate or change?**

- Added Balanced, Genre-First, and Mood-First scoring strategies using the
  Strategy design pattern. `RANKING_MODE` in `src/main.py` selects the mode.
- Added a one-point penalty each time an artist is already represented in the
  selected recommendations, and included it in the score explanation.
- Documented how the penalty promotes variety and its limits as a fairness
  measure.
- Added popularity, release decade, detailed mood tags, vocal style, and
  lyrical theme to all 18 rows in `data/songs.csv`.
- Converted the new numeric fields and mood tags in `load_songs`.
- Added corresponding preferences and score reasons for the new attributes.
- Connected the existing acoustic preference to acousticness.
- Updated profile examples, tests, the README outputs, and the model card.

**What did you verify or fix manually?**

#I checked that the CSV has 18 songs and that the new columns have useful
values. I reviewed the weights and confirmed that a full-match feature score can reach 7.5 before the artist penalty. I tested that the penalty moves a different artist ahead of a repeated artist and appears in the reason text. I ran each ranking strategy with the pop profile and confirmed Genre-First moves “Gym Hero” ahead of “Rooftop Lights.” Mood-First adds a bonus to songs with the preferred mood. I also ran the recommender for all three named profiles, ran the tests, and checked the documentation diff for formatting.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

#Strategy

**How did AI help you brainstorm or implement it?**

#The request called for multiple interchangeable ranking modes. The AI
suggested the Strategy pattern so each mode could implement the same scoring interface, while the recommendation function could use any selected strategy.

**How does the pattern appear in your final code?**

`RankingStrategy` defines the scoring interface in `src/recommender.py`.
`BalancedStrategy`, `GenreFirstStrategy`, and `MoodFirstStrategy` implement
it. `RANKING_STRATEGIES` provides the choices, and `RANKING_MODE` in
`src/main.py` lets the user switch between them.
