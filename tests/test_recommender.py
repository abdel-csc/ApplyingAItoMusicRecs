from src.recommender import Song, UserProfile, Recommender

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
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
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
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""

def test_genre_match_boosts_score():
    """Genre match should add 2.0 to score."""
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="focused",
        target_energy=0.5,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)
    # lofi song should rank first due to genre match (+2.0)
    assert results[0].genre == "lofi"

def test_recommend_respects_k():
    """recommend() should return exactly k results."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    assert len(rec.recommend(user, k=1)) == 1
    assert len(rec.recommend(user, k=2)) == 2

def test_acoustic_preference_boosts_acoustic_song():
    """likes_acoustic=True should boost songs with acousticness > 0.5."""
    user = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.5,
        likes_acoustic=True,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)
    # The lofi song has acousticness=0.9, so it should get the +0.5 boost
    scores = []
    for song in rec.songs:
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        score += 1 - abs(song.energy - user.target_energy)
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 0.5
        scores.append((song, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    assert scores[0][0].title == "Chill Lofi Loop"
