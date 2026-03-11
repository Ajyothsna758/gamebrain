import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from games.models import Game
from userpanel.models import UserPreference


def ml_new_user_recommendations(user, limit=20):

    games = Game.objects.prefetch_related(
        "genres",
        "themes",
        "platforms",
        "player_perspectives"
    )

    game_data = []

    for g in games:
        features = []

        features += [genre.name for genre in g.genres.all()]
        features += [theme.name for theme in g.themes.all()]
        features += [platform.name for platform in g.platforms.all()]
        features += [p.name for p in g.player_perspectives.all()]

        game_data.append({
            "id": g.id,
            "game": g,
            "features": " ".join(features)
        })

    df = pd.DataFrame(game_data)

    # Vectorize features
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["features"])

    try:
        pref = UserPreference.objects.get(user=user)

        user_features = []

        user_features += [g.name for g in pref.preferred_genres.all()]
        user_features += [t.name for t in pref.preferred_themes.all()]
        user_features += [p.name for p in pref.preferred_platform.all()]
        user_features += [pp.name for pp in pref.preferred_player_perspective.all()]

        user_text = " ".join(user_features)

    except UserPreference.DoesNotExist:
        return []

    # Transform user preferences into vector
    user_vector = vectorizer.transform([user_text])

    # Compute similarity
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    df["score"] = similarity_scores

    df = df.sort_values(by="score", ascending=False)

    results = []

    for _, row in df.head(limit).iterrows():
        results.append({
            "game": row["game"],
            "score": float(row["score"]),
            "explanations": ["Matches your preferred genres/themes/platforms"]
        })

    return results