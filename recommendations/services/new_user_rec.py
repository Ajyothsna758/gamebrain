from games.models import Game
from userpanel.models import UserPreference
from django.db.models import Q


def new_user_recommendations(user, limit=100):
    games = Game.objects.all()
    q=Q()
    try:
        prefer = UserPreference.objects.get(user = user)
        if prefer.preferred_genres.exists():
            q|= Q(genres__in = prefer.preferred_genres.all())
        if prefer.preferred_platform.exists():
            q|= Q(platforms__in = prefer.preferred_platform.all())
        if prefer.preferred_player_perspective.exists():
            q|= Q(player_perspectives__in = prefer.preferred_player_perspective.all())
        if prefer.preferred_themes.exists():
            q|= Q(themes__in = prefer.preferred_themes.all()) 
        print(q)         
    except UserPreference.DoesNotExist:
        pass
    return games.filter(q).order_by("-total_rating", "-released").distinct()[:limit]
                      
# def new_user_recommendations(user, limit=100):
#     games = Game.objects.all()
#     q=Q()
#     try:
#         prefer = UserPreference.objects.get(user = user)
#         if prefer.preferred_genres.exists():
#             games= games.filter(genres__in = prefer.preferred_genres.all())
#         if prefer.preferred_platform.exists():
#             games= games.filter(platforms__in = prefer.preferred_platform.all())
#         if prefer.preferred_player_perspective.exists():
#             games= games.filter(player_perspectives__in = prefer.preferred_player_perspective.all())
#         if prefer.preferred_themes.exists():
#             games= games.filter(themes__in = prefer.preferred_themes.all()) 
#         print(games)     
#     except UserPreference.DoesNotExist:
#         pass
#     return games.order_by("-total_rating", "-released").distinct()[:limit]
                      
