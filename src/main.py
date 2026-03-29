"""
Command line runner for the Music Recommender Simulation.
"""
from recommender import load_songs, recommend_songs


def run_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"  Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Profile 1: High-Energy Pop (default)
    run_profile("High-Energy Pop", {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8
    }, songs)

    # Profile 2: Chill Lofi
    run_profile("Chill Lofi", {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35
    }, songs)

    # Profile 3: Intense Rock
    run_profile("Intense Rock", {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9
    }, songs)

    # Profile 4: Edge case - conflicting prefs
    run_profile("Conflicting (sad + high energy)", {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9
    }, songs)


if __name__ == "__main__":
    main()
