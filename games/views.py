from django.shortcuts import render

# Create your views here.
from .models import Game, UserGameRating
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def games_list(request):
    games= Game.objects.all()
    user_ratings={}
    if request.user.is_authenticated:
        user_ratings={
            r.game_id: r.rating for r in UserGameRating.objects.filter(user=request.user)
        }
    return render(request, "games/games.html", {"games":games, "user_ratings":user_ratings})
    
    