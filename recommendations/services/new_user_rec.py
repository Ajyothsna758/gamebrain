from games.models import Game
from userpanel.models import UserPreference

def new_user_recommendations(user):
    games = Game.objects.all()
    try:
        prefer = UserPreference.objects.get(user = user)
        if prefer.preferred_genres.exists():
            games= games.filter(genres__in = prefer.preferred_genres.all())
        if prefer.preferred_platform.exists():
            games= games.filter(platforms__in = prefer.preferred_platform.all())
        if prefer.preferred_player_perspective.exists():
            games= games.filter(player_perspectives__in = prefer.preferred_player_perspective.all())
        if prefer.preferred_themes.exists():
            games= games.filter(themes__in = prefer.preferred_themes.all())  
    except UserPreference.DoesNotExist:
        pass
    return games.order_by("-total_rating", "-released").distinct()
                      
