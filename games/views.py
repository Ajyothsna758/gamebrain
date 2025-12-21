from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Game, UserGameRating, WishList
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def games_list(request):
    games= Game.objects.all()
    # rating
    user_ratings={}
    if request.user.is_authenticated:
        user_ratings={
            r.game_id: r.rating for r in UserGameRating.objects.filter(user=request.user)
        }
    # wishlist
    wishlist_games=WishList.objects.filter(user=request.user).values_list("game_id", flat=True)
        
    return render(request, "games/games.html", 
                  {"games":games, "user_ratings":user_ratings, 
                   "wishlist_games": wishlist_games})
   
    
# to add or remove game from wishlist page by clicking on image    
@login_required
def toggle_wishlist(request, game_id):
    game= get_object_or_404(Game, id=game_id)
    wishlist_game= WishList.objects.filter(user=request.user, game=game)
    if wishlist_game.exists():
        wishlist_game.delete()
    else:
        WishList.objects.create(user=request.user, game=game)       
    return redirect(request.META.get("HTTP_REFERER", "games"))   
 
@login_required
def wishlist(request):
    wishlist_items= WishList.objects.filter(user=request.user).select_related("game")
    wishlist_games= wishlist_items.values_list("game_id", flat=True)
    return render(request, "games/wishlist.html", 
                  {"wishlist_games": wishlist_games,
                   "wishlist_items":wishlist_items}) 
    
    
    
    
@login_required
def check_svg(request):
    return render(request, "games/1.html")    