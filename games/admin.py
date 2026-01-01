from django.contrib import admin

# Register your models here.
from .models import Game, UserLibrary, GameStatus, GameOverallRating, RatingCategory, RatingType, GameCategoryRating 
#admin.site.register(Game)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name", "developer", "publisher")
    
admin.site.register(GameStatus)
admin.site.register(UserLibrary)   
admin.site.register(RatingCategory)
admin.site.register(RatingType) 
admin.site.register(GameOverallRating)
admin.site.register(GameCategoryRating)
    
    