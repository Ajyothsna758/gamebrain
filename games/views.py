from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Game, WishList, GameStatus, UserLibrary, RatingCategory, RatingType, GameOverallRating, GameCategoryRating
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator

# games
@login_required
def games_list(request):
    games= Game.objects.all().order_by("-released")
    paginator= Paginator(games, 20)
    page_number= request.GET.get("page")
    games_page= paginator.get_page(page_number)
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
                  {"games":games_page,
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
    
#  overall ratings
@login_required
@require_POST
def save_overall_rating(request):
    game_id= request.POST.get("game_id")
    rating_id= request.POST.get("rating_id")
    
    game= get_object_or_404(Game, id=game_id)
    rating_id= int(rating_id) #ensure rating_id is integer for comparison
    
    # save whole block at once in db (to avoid partial records)
    with transaction.atomic():
        record=GameOverallRating.objects.filter(user=request.user, game=game).first()
        # check record is present or not in table
        if record:
            if record.rating_type_id == rating_id:
                # user clicked on active button (delete)
                record.delete()
                action="deleted"
            else:
                # user clicked on another button (update) 
                updated_rating= get_object_or_404(RatingType, id=rating_id)
                record.rating_type= updated_rating
                record.save()
                action="saved"
        else:
            new_rating= get_object_or_404(RatingType, id=rating_id) 
            GameOverallRating.objects.create(
                user=request.user,
                game=game,
                rating_type=new_rating
            )  
            action="saved" 
    return JsonResponse({
        "success": True,
        "action": action,
        "avg":game.overall_average(),
        "label":game.overall_label(),
        "breakdown": game.overall_breakdown(),
        "rating_image":game.overall_rating_image(),
    })    

# category rating               
@login_required
@require_POST
def save_category_rating(request):
    game_id= request.POST.get("game_id")
    rating_id= request.POST.get("rating_id") 
    category_id= request.POST.get("category_id")
    
    game= get_object_or_404(Game, id=game_id)
    category= get_object_or_404(RatingCategory, id=category_id)
    rating_id= int(rating_id)
    
    with transaction.atomic():
        record= GameCategoryRating.objects.filter(user= request.user, game=game, category=category).first()
        # check record present or not
        if record:
            # click on selected rating (delete)
            if record.rating_type_id == rating_id:
                record.delete()
                action="deleted"
            # clicked on another rating    
            else:
                updated_rating= get_object_or_404(RatingType, id=rating_id)
                record.rating_type= updated_rating
                record.save()
                action="saved"
        else:
            new_rating= get_object_or_404(RatingType, id=rating_id)
            GameCategoryRating.objects.create(
                user=request.user,
                game=game,
                category=category,
                rating_type=new_rating
            )
            action="saved"
    return JsonResponse({
        "success":True,
        "action":action,
        "category": category.key,
        "category_avg": game.category_average(category.key),
        "category_breakdown": game.category_breakdown(category),
    })        
            
                 
# search
def game_search_autocomplete(request):
    word = request.GET.get("word", "").strip()
    games = (Game.objects.filter(name__icontains=word).only("id", "name", "cover_url", "igdb_id"))[:10]
    data= [{
        "id": game.id,
        "name": game.name,
        "igdb_id": game.igdb_id,
        "cover_url": game.cover_url
    }
           for game in games
           ]
    return JsonResponse(data, safe=False)

def game_search(request):
    search = request.GET.get("search", "").strip()
    print(search)
    games_page = Game.objects.none()
    results= 0
    if search:
        games = Game.objects.filter(name__icontains=search)
        paginator= Paginator(games, 20)
        page_number= request.GET.get("page")
        games_page= paginator.get_page(page_number) 
        results= games.count()
           
    return render(request, "games/search_games.html",{"games":games_page, "search":search, "count":results })

    