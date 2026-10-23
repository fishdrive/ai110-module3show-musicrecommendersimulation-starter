# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

#MusicTaster

## 2. Intended Use  

#This tool ranks songs by a listener's preferences and explains each result. It is for classroom learning, not real-world recommendations. It assumes the song tags are correct and that one profile can represent a listener's taste.

## 3. How the Model Works  

#The recommender checks genre, mood, energy, and acousticness. It also checks popularity, release decade, detailed mood tags, vocal style, and lyrical theme. Genre and mood matches add one point each. Energy closeness adds up to two points. Popularity closeness adds up to one point. A matching decade, mood tag, vocal style, lyrical theme, or acoustic preference adds half a point. The system adds the points and ranks the songs. It also lists the reasons for each score. The feature score can reach 7.5 points. During ranking, each earlier recommendation by the same artist subtracts one point. This helps the list include more artists.

The original recipe gave genre more weight and energy less weight. The current recipe halves the genre points and doubles the energy points. The added song features now affect the scores too. The user can choose Balanced, Genre-First, or Mood-First ranking. Genre-First gives an extra bonus for a favorite genre. Mood-First gives an extra bonus for a favorite mood.

## 4. Data  

#The catalog has 18 songs. It includes pop, rock, lofi, jazz, classical, folk, and other genres. Each song has genre, mood, energy, tempo, valence,
danceability, and acousticness. Five added fields are popularity, release
decade, detailed mood tags, vocal style, and lyrical theme. The catalog does not include real listening history or actual lyrics.

---

## 5. Strengths  

#The system works well when a listener's genre and mood are in the catalog.
The pop and happy profile ranked matching songs near the top. Extra song
features help distinguish songs with similar genres and energy. The artist
penalty also helps prevent one artist from taking several top spots.

---

## 6. Limitations and Bias 



#The catalog is small, and its popularity values are made up for this project. Energy has more weight than genre, so it can dominate a ranking. The system uses exact matches for many tags, so similar labels may not match. It does not check whether user targets are within the expected ranges. The artist penalty encourages variety in one list, but it is only a small fairness step. It does not guarantee equal exposure for all artists or genres.


---

## 7. Evaluation  


#I tested the High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles. Each put songs with matching preferences near the top. I also tested profiles with unavailable labels and out-of-range energy targets. Those tests showed that energy can dominate when labels do not match, and that invalid targets can still affect scores.

### Comparing Profile Results

| Profiles compared | What changed, and why |
|---|---|
| High-Energy Pop vs. Chill Lofi | Pop favors “Sunrise City.” Lofi favors “Library Rain,” which matches its genre, mood, acoustic preference, and low energy target. The repeat-artist penalty also makes room for other artists in the lofi top five. |
| Chill Lofi vs. Deep Intense Rock | The lofi profile favors calm songs. The rock profile favors “Storm Runner,” which matches its rock, intense, high-energy preferences. |
| High-Energy Pop vs. Deep Intense Rock | Both prefer energetic music, but their genre, mood, decade, and detailed tags differ. Those matches help “Sunrise City” and “Storm Runner” lead their lists. |

---

## 8. Future Work  

#I would use real song data and validate preference ranges. I would also add more songs and test how each ranking mode affects recommendation variety.

---

## 9. Personal Reflection  

#I learned that recommendation systems can use different methods. I was
surprised that a simple score could find songs I might like. I also learned that choosing the features is an important part of designing a recommender.
