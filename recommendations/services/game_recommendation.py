from recommendations.services.existing_user_rec import existing_user_recommendations
from recommendations.services.new_user_rec import new_user_recommendations
from games.models import UserLibrary, WishList, GameOverallRating

def get_recommendations(user, limit=100):
    library_games = UserLibrary.objects.filter(user=user).values_list("game_id", flat=True)
    WishList_games= WishList.objects.filter(user=user).values_list("game_id", flat=True)
    rated_games= GameOverallRating.objects.filter(user=user).values_list("game_id", flat=True)
    has_history= set(library_games) | set(WishList_games) | set(rated_games)
    
    if has_history:
        return existing_user_recommendations(user, limit=100)
    else:
        return new_user_recommendations(user, limit=100)
    
    
    
    