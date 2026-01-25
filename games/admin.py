from django.contrib import admin

# Register your models here.
from .models import Game, UserLibrary, GameStatus, GameOverallRating, RatingCategory, RatingType, GameCategoryRating, WishList, Genre, Platform, PlayerPerspective, Company, Franchise, Collection, GameMode, GameTimeToBeat, Keyword, Theme
#admin.site.register(Game)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name", "igdb_rating", "igdb_url")
    
admin.site.register(GameStatus)
admin.site.register(UserLibrary)   
admin.site.register(RatingCategory)
admin.site.register(RatingType) 
admin.site.register(GameOverallRating)
admin.site.register(GameCategoryRating)
admin.site.register(WishList)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(PlayerPerspective)
admin.site.register(Franchise)
admin.site.register(Collection)
admin.site.register(Company)
admin.site.register(GameMode)
admin.site.register(GameTimeToBeat)
admin.site.register(Keyword)
admin.site.register(Theme)
    
    