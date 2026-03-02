from django.db.models import Q
from games.models import Game, Genre, Platform, Theme


# get seeded or user preferred game ids
def get_user_seed_games(user, min_rating_weight=3):
    wishlist_game_ids = Game.objects.filter(wishlist__user=user).values_list("id", flat=True)
    library_game_ids = Game.objects.filter(userlibrary__user=user).exclude(userlibrary__status__name="Dropped").values_list("id", flat=True)
    highrated_game_ids = Game.objects.filter(overall_ratings__user=user, overall_ratings__rating_type__weight__gte=min_rating_weight).values_list("id", flat=True)
    print(f"wishlist_ids: {wishlist_game_ids}")
    print(f"libraryIids: {library_game_ids}")
    print(f"high rated ids: {highrated_game_ids}")
    seed_ids= set(wishlist_game_ids) | set(library_game_ids) | set(highrated_game_ids)
    print(seed_ids)
    return Game.objects.filter(id__in=seed_ids)

# extract games meta data
def extract_games_metadata(seeds):
    return {
        "genres": set(seeds.values_list("genres__id", flat=True)),
        "platforms": set(seeds.values_list("platforms__id", flat=True)),
        "game_modes": set(seeds.values_list("game_modes__id", flat=True)),
        "player_perspectives": set(seeds.values_list("player_perspectives__id", flat=True)),
        "themes": set(seeds.values_list("themes__id", flat=True)),
        "franchises": set(seeds.values_list("franchises__id", flat=True)),
        "similar_games": set(seeds.values_list("similar_games__id", flat=True)),
        "seed_ids": set(seeds.values_list("id", flat=True)),
    }

# get candidate games from games database    
def get_candidate_games(games_metadata, limit=500):
    """
    get candidate games from all games data base which matches user preferences
    """
    q=Q()
    if games_metadata["genres"]:
        q &= Q(genres__in= games_metadata["genres"])
    if games_metadata["platforms"]:
        q &= Q(platforms__in= games_metadata["platforms"])
    if games_metadata["game_modes"]:
        q |= Q(game_modes__in= games_metadata["game_modes"])   
    if games_metadata["player_perspectives"]:
        q &= Q(player_perspectives__in= games_metadata["player_perspectives"])
    if games_metadata["themes"]:
        q |= Q(themes__in= games_metadata["themes"])
    if games_metadata["franchises"]:
        q |= Q(franchises__in = games_metadata["franchises"])
    if games_metadata["similar_games"]:
        q &= Q(similar_games__in= games_metadata["similar_games"])    
    print(q)
    return (Game.objects.filter(q)\
            .exclude(id__in=games_metadata["seed_ids"])\
            .prefetch_related("genres", "platforms", "game_modes", "player_perspectives","themes", "franchises", "similar_games")\
            .only("id", "cover_url", "total_rating", "name")
            .distinct()[:limit]) 
                         
# game scores 
def calculate_game_score(game, games_metadata):
    reasons=[]
    score=0
    genre_ids = {g.id for g in game.genres.all()}
    platform_ids = {p.id for p in game.platforms.all()}
    game_mode_ids = {gm.id for gm in game.game_modes.all()}
    player_perspective_ids = {pp.id for pp in game.player_perspectives.all()}
    theme_ids ={t.id for t in game.themes.all()}
    franchise_ids = {f.id for f in game.franchises.all()}
    similar_game_ids = {sg.id for sg in game.similar_games.all()}
    common_genres = genre_ids & games_metadata["genres"]
    if common_genres:
        score += len(common_genres)*4
        reasons.append("Matches your preferred genres")
    common_platforms = platform_ids & games_metadata["platforms"] 
    if common_platforms:
        score += len(common_platforms)*5
        reasons.append("Matches your preferred platforms")
    common_game_modes = game_mode_ids & games_metadata["game_modes"] 
    if common_game_modes:
        score += len(common_game_modes)*3
        reasons.append("Matches your preferred game modes")
    common_player_perspectives = player_perspective_ids & games_metadata["player_perspectives"] 
    if common_player_perspectives:
        score += len(common_player_perspectives)*3
        reasons.append("Matches your preferred player perspectives")
    common_themes = theme_ids & games_metadata["themes"] 
    if common_themes:
        score += len(common_themes)*3
        reasons.append("Matches your preferred themes")
    common_franchises = franchise_ids & games_metadata["franchises"] 
    if common_franchises:
        score += len(common_franchises)*4 
        reasons.append("Matches your preferred franchises")  
    common_similar_games = similar_game_ids & games_metadata["similar_games"]   
    if common_similar_games:
        score += len(common_similar_games)*6  
    
    # if game.total_rating:
    #     score += game.total_rating/20     
    print(game.id, game.name, score)    
    return score, reasons       
           

def existing_user_recommendations(user, limit=10):
    seeds = get_user_seed_games(user)
    if not seeds.exists():
        print("No seed games found for user")
        return []
    games_metadata = extract_games_metadata(seeds)
    candidates = get_candidate_games(games_metadata, limit=10000)
    scored_candidates = []
    for game in candidates:
        score, reasons = calculate_game_score(game, games_metadata)
        if score > 0:
            scored_candidates.append((game, score, reasons))

    # Sort by score descending
    scored_candidates.sort(key=lambda x: x[1], reverse=True)

    # Return top N
    top_games = [
        {"game": game, "score": score, "explanations": reasons}
        for game, score, reasons in scored_candidates[:limit]
    ]

    print(f"Returning {len(top_games)} top recommendations")
    print(candidates.count())
    return top_games