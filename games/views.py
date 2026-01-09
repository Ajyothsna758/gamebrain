from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Game, WishList, GameStatus, UserLibrary, RatingCategory, RatingType, GameOverallRating, GameCategoryRating
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def games_list(request):
    games= Game.objects.all()
    # wishlist
    wishlist_games=WishList.objects.filter(user=request.user).values_list("game_id", flat=True)
    # library
    statuses= GameStatus.objects.all()
    library_games= {
        lg.game_id: lg for lg in UserLibrary.objects.filter(user=request.user) 
    }
    # rating
    rating_types= RatingType.objects.all()
    overall_rating = {
        r.game_id: r.rating_type_id for r in GameOverallRating.objects.filter(user=request.user)
    }
    categories= RatingCategory.objects.all()
    # category_rating= {
    #     (r.game_id, r.category_id): r.rating_type_id for r in GameCategoryRating.objects.filter(user=request.user)
    # }
    category_rating = {}
    for r in GameCategoryRating.objects.filter(user=request.user):
        category_rating.setdefault(r.game_id, {})[r.category_id] = r.rating_type_id
    
    return render(request, "games/games.html", 
                  {"games":games,
                   "wishlist_games": wishlist_games,
                   "statuses":statuses,
                   "library_games":library_games,
                   "rating_types":rating_types,
                   "overall_rating":overall_rating,
                   "category_rating":category_rating,
                   "categories":categories,
                   })
    
   

### wishlist    
# to add or remove game from wishlist page by clicking on image    
@login_required
def toggle_wishlist(request, game_id):
    game= get_object_or_404(Game, id=game_id) 
    UserLibrary.objects.filter(user=request.user, game=game).delete()
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
    WishList.objects.filter(user=request.user, game=game).delete()
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
    
# ratings
@login_required
@require_POST
def save_overall_rating(request):
    game_id= request.POST.get("game_id")
    rating_id= request.POST.get("rating_id")
    
    game= get_object_or_404(Game, id=game_id)
    rating= get_object_or_404(RatingType, id=rating_id)
    
    GameOverallRating.objects.update_or_create(
        user=request.user,
        game=game,
        defaults={"rating_type": rating}
    )
    return JsonResponse({
        "success": True,
        "avg": game.overall_average(),
        "label": game.overall_label(),
        "breakdown": game.overall_breakdown(),
        "rating_image": game.overall_rating_image(),
        
        })
                
@login_required
@require_POST
def save_category_rating(request):
    game_id= request.POST.get("game_id")
    rating_id= request.POST.get("rating_id") 
    category_id= request.POST.get("category_id")
    
    game= get_object_or_404(Game, id=game_id)
    category= get_object_or_404(RatingCategory, id=category_id)
    rating= get_object_or_404(RatingType, id=rating_id)
    
    GameCategoryRating.objects.update_or_create(
        user=request.user,
        game=game,
        category= category,
        defaults={
            "rating_type":rating,
        }
    )
    return JsonResponse({
        "success":True,
        "category": category.key,
        "category_avg": game.category_average(category.key),
        "category_breakdown": game.category_breakdown(category),
        
    })
                 
