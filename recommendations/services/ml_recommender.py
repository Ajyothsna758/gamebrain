import pandas as pd
import numpy as np
from games.models import Game
from .existing_user_rec import get_user_seed_games
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MLExistingUserRecommendation:
    def __init__(self):
        games= Game.objects.prefetch_related("platforms", "themes", "genres", "player_perspectives", "game_modes", "similar_games", "franchises").all()
        games_data = []
        # fetch all game meta_data
        for g in games:
            features=[]
            features.extend([p.name for p in g.platforms.all()])
            features.extend([t.name for t in g.themes.all()])
            features.extend([genre.name for genre in g.genres.all()])
            features.extend([pp.name for pp in g.player_perspectives.all()])
            features.extend([gm.name for gm in g.game_modes.all()])
            features.extend([f.name for f in g.franchises.all()])
            features.extend([d.name for d in g.developer.all()])
            features.extend([pub.name for pub in g.publisher.all()])
            text = " ".join(features)
            games_data.append({
                "id":g.id,
                "name": g.name,
                "features": text
            })
        self.df = pd.DataFrame(games_data)   #Converts the list of dictionaries into a pandas DataFrame
        self.vectorizer = TfidfVectorizer(stop_words="english") # convert text to numerical vectors
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["features"])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix) # Compare each game vector with every other game vector
        self.game_index = pd.Series(self.df.index, index=self.df["id"]) #map game id -> dataframe index
    
    def recommended(self, seed_game_ids, limit=10):
        indexes = [self.game_index[gid] for gid in seed_game_ids if gid in self.game_index]
        if not indexes:
            return []
        # calculate similarity scores
        sim_scores = np.mean(self.similarity_matrix[indexes], axis=0)
        scored_games = list(enumerate(sim_scores))
        scored_games = sorted(scored_games, key=lambda x: x[1], reverse=True)
        results=[]
        for idx, score in scored_games:
            game_id = self.df.iloc[idx]["id"]
            if game_id not in seed_game_ids:
                results.append((game_id, score))
            if len(results) >= limit:
                break
        game_ids = [gid for gid, _ in results]
        games = Game.objects.filter(id__in=game_ids)
        return [
            {
                "game": g,
                "score": dict(results)[g.id],
                "explanations": ["Similar to your played games"]
            }
            for g in games
        ]

recommender = MLExistingUserRecommendation()

def ml_existing_user_recommendations(user, limit=500):
    seed_games = get_user_seed_games(user)
    seed_ids = list(seed_games.values_list("id", flat=True))
    if not seed_ids:
        return []
    return recommender.recommended(seed_ids, limit)         
            