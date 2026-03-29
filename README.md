# 🎵 Music Recommender Simulation

## Project Summary


This project builds a content-based music recommender system that scores songs 
against a user's taste profile and returns the top matches. It uses three song 
attributes (genre, mood, and energy) to calculate a weighted score for each 
song in the catalog. The system ranks all songs by score and returns the top 5 
recommendations along with an explanation of why each song was suggested.

## How The System Works

Each Song in the system has the following features:
- Genre: musical category (pop, rock, lofi, jazz, etc.)
- Mood: emotional tone (happy, chill, intense, relaxed, etc.)
- Energy: a 0.0 to 1.0 scale of intensity
- Tempo_bpm, valence, danceability, acousticness are all additional attributes
- Ratings: Crucial for scale, which I touched upon in energy.

The `UserProfile` stores:
- `favorite_genre`: the genre the user prefers
- `favorite_mood`: the mood the user prefers
- `target_energy`: the energy level the user wants (0.0 to 1.0)
- `likes_acoustic`: whether the user prefers acoustic songs

The Recommender's task is to compute a score for each song using this formula:
- Genre match: +2.0 points
- Mood match: +1.0 point
- Energy closeness: `1 - abs(song_energy - target_energy)` (between 0.0 and 1.0)
- Acoustic preference match: +0.5 points (if applicable)

Songs are then sorted from highest to lowest score and the top 5 are returned 
with an explanation of which factors contributed to each score.

Data flow:
User Prefs -> score every song -> sorts by score -> returning the top 5

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

## Experiments You Tried

Here are a few experiments i've tried:

- **Default pop/happy profile:** Sunrise City ranked #1 with a near-perfect 
  score of 3.98. Genre, mood, and energy all matched closely. This confirmed 
  the scoring logic was working correctly.

- **Chill lofi profile:** Library Rain scored a perfect 4.0 because its energy 
  (0.35) exactly matched the user's target. Showed that energy similarity can 
  be a tiebreaker when genre and mood both match.

- **Intense rock profile:** Only one rock song exists in the dataset (Storm Runner), 
  so positions 2-5 were filled by non-rock songs ranked purely by energy. This 
  revealed a dataset imbalance problem.

- **Conflicting profile (sad mood + high energy):** No song matched both 
  preferences, so genre (+2.0) dominated. Gym Hero and Sunrise City topped the 
  list despite being "intense" and "happy." Neither matched the sad mood at all.

  What this taught me especially is that even if we do not get the outcome we're looking for, it's important to constantly conduct tests to arrive at general conclusions. This is especially important when working with AI, or even in the Data science ML field.

---

## Limitations and Risks


- The catalog only has 10 songs, which is far too small for real use. Genres 
  like rock (1 song) and jazz (1 song) are severely underrepresented.
- Genre has the highest weight (+2.0), so it almost always dominates the 
  ranking even when mood and energy are a better fit.
- The system has no memory. It treats every recommendation session as if the 
  user is brand new with no listening history.
- It does not understand lyrics, language, or cultural context at all.
- Users who prefer underrepresented genres will consistently get worse 
  recommendations than pop fans.

---

## Reflection


Building this recommender made it clear how much a simple scoring formula can 
shape what users see and what they never see. Genre's +2.0 weight meant it 
almost always determined the top results, even when other attributes were a 
better fit. This mirrors a real risk in production systems: whatever features 
get the highest weight end up defining the user's entire experience, often in 
ways the user never notices.

Bias showed up in an unexpected place, not in the algorithm itself, but in 
the data. Rock and jazz fans got poor recommendations simply because those 
genres had fewer songs in the catalog. In a real platform serving millions of 
users, that kind of imbalance could systematically disadvantage listeners whose 
tastes don't match the majority of the dataset.
## Screenshots

### Phase 3: Default Profile Run
![Single Profile Run](images/singleprofilerun.png)

### Phase 4: High-Energy Pop
![High Energy Pop](images/highenergypop.png)

### Phase 4: Chill Lofi
![Chill Lofi](images/chill_lofi.png)

### Phase 4: Intense Rock
![Intense Rock](images/intenserock.png)

### Phase 4: Conflicting Profile (sad + high energy)
![Conflicting Profile](images/conflicting_sad_high_energy.png)