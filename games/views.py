from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Game, UserGameRating, WishList, GameStatus, UserLibrary
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
    # library
    statuses= GameStatus.objects.all()
    library_games= {
        lg.game_id: lg for lg in UserLibrary.objects.filter(user=request.user) 
    }
    return render(request, "games/games.html", 
                  {"games":games, "user_ratings":user_ratings, 
                   "wishlist_games": wishlist_games,
                   "statuses":statuses,
                   "library_games":library_games})
    
   

### wishlist    
# to add or remove game from wishlist page by clicking on image    
@login_required
def toggle_wishlist(request, game_id):
    game= get_object_or_404(Game, id=game_id) 
    obj, created= WishList.objects.get_or_create(user=request.user, game=game)
    if not created:
        obj.delete()
              
    return redirect(request.META.get("HTTP_REFERER", "games"))   
 
@login_required
def wishlist(request):
    wishlist_items= WishList.objects.filter(user=request.user).select_related("game")
    wishlist_games= wishlist_items.values_list("game_id", flat=True)
    library_games= UserLibrary.objects.filter(user=request.user).values_list("game_id",flat=True)
    return render(request, "games/wishlist.html", 
                  {"wishlist_games": wishlist_games,
                   "wishlist_items":wishlist_items,
                   "library_games": library_games,
                   }) 
    
       
### My Library
@login_required
def toggle_library(request, game_id):
    game= get_object_or_404(Game, id=game_id)
    status=get_object_or_404(GameStatus, name__iexact="Uncategorized")
    obj, created= UserLibrary.objects.get_or_create(
        user=request.user,
        game=game,
        defaults={
            "status": status
        } 
    )
    if not created:
        obj.delete()
    return redirect(request.META.get("HTTP_REFERER", "games"))    

@login_required
def update_library_status(request, game_id, status_id):
    game=get_object_or_404(Game, id=game_id)
    status=get_object_or_404(GameStatus, id=status_id)
    library, _= UserLibrary.objects.get_or_create(
        user=request.user,
        game=game,
        defaults={
            "status":status
        }
    )
    library.status= status
    library.save()
    return redirect(request.META.get("HTTP_REFERER", "games"))
      

@login_required
def library(request, status_id=None):
    library_items= UserLibrary.objects.filter(user=request.user).select_related("game", "status")
    library_games= library_items.values_list("game_id", flat=True)
    wishlist_games=WishList.objects.filter(user=request.user).values_list("game_id", flat=True)
    statuses= GameStatus.objects.all()
    if status_id:
        library_items=library_items.filter(status_id=status_id)
    return render(request, "games/library.html",{
        "statuses":statuses,
        "library_items":library_items,
        "library_games":library_games,
        "active_status":status_id,
        "wishlist_games": wishlist_games,
    })  
    
             
    
               
