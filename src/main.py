"""
Command line runner for the Music Recommender Simulation.
Extended with RAG (LLM explanations), confidence scoring, and logging.
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs
from llm_explainer import explain_recommendations

# Set up logging
logging.basicConfig(
    filename='recommender.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

MAX_SCORE = 4.5  # genre(2.0) + mood(1.0) + energy(1.0) + acoustic(0.5)


def get_confidence(score: float) -> float:
    return round(score / MAX_SCORE, 2)


def run_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"{'='*50}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rec in recommendations:
        song, score, explanation = rec
        confidence = get_confidence(score)
        print(f"{song['title']} - Score: {score:.2f} | Confidence: {confidence:.0%}")
        print(f"  Because: {explanation}")
        print()

    # RAG: ask Gemini to explain the full set of recommendations
    print("Gemini says:")
    llm_explanation = explain_recommendations(user_prefs, recommendations)
    print(llm_explanation)

    # Log the session
    top_song = recommendations[0][0]['title']
    top_score = recommendations[0][1]
    top_confidence = get_confidence(top_score)
    logging.info(
        f"Profile: {profile_name} | Top song: {top_song} | "
        f"Score: {top_score:.2f} | Confidence: {top_confidence:.0%}"
    )


def main() -> None:
    songs = load_songs("data/songs.csv")

    run_profile("High-Energy Pop", {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8
    }, songs)

    run_profile("Chill Lofi", {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35
    }, songs)

    run_profile("Intense Rock", {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9
    }, songs)

    run_profile("Conflicting (sad + high energy)", {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9
    }, songs)


if __name__ == "__main__":
    main()
