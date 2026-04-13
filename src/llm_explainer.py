import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_recommendations(user_prefs: dict, top_songs: list) -> str:
    song_list = "\n".join(
        f"- {s['title']} by {s['artist']} (genre: {s['genre']}, mood: {s['mood']}, energy: {s['energy']})"
        for s, score, explanation in top_songs
    )
    prompt = f"""A music listener has the following taste profile:
- Favorite genre: {user_prefs['genre']}
- Favorite mood: {user_prefs['mood']}
- Target energy level: {user_prefs['energy']} (scale 0.0 to 1.0)

Based on their profile, here are their top 5 recommended songs:
{song_list}

In 3-4 sentences, explain why these songs are a good match for this listener. Be specific about genre, mood, and energy."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LLM explanation unavailable: {e}]"
