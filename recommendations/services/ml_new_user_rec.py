import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from games.models import Game
from userpanel.models import UserPreference


def ml_new_user_recommendations(user, limit=500):
    # get user preferences
    try:
        pref = UserPreference.object.get(user=user)
        user_features = []
        user_features.extend([genre.name for genre in pref.preferred_genres.all()])
        user_features.extend([t.name for t in pref.preferred_themes.all()])
        user_features.extend([pp.name for pp in pref.preferred_player_perspective.all()])
        user_features.extend([p.name for p in pref.platform.all()])
    except UserPreference.DoesNotExist:
        user_features = []
        
    # top rated if no preferences
    if not user_features:
        top_games = Game.objects.order_by("-total_rating")[:limit]
        return [{
            "game":g,
            "score": g.total_rating,
            "explanations": ["top rated games"]
        }
                for g in top_games
                ] 
    # Otherwise compute similarity using metadata 
    games = Game.objects.prefetch_related("genres", "themes", "platforms","player_perspectives")
    games_data = []
    for g in games:
        features = []
        features.extend([genre.name for genre in g.genres.all()])
        features.extend([t.name for t in g.themes.all()])
        features.extend([p.name for p in g.platforms.all()])
        features.extend([pp.name for pp in g.player_perspectives.all()])
        text = " ".join(features)
        games_data.append({
            "id":g.id,
            "name": g.name,
            "features": text
        })
    df = pd.DataFrame(games_data)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["features"]) 
    user_text = " ".join(user_features)
    user_vector = vectorizer.transform([user_text])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    df["score"] = similarity_scores
    df_sorted = df.sort_values(by="score", ascending=False)
    results = []
    for _, row in df_sorted.head(limit).iterrows():
        results.append({
            "game": row["game"],
            "score": float(row["score"]),
            "explanations": ["Matches your preferred genres/themes/platforms"]
        })

    return results   
            