from django.contrib import admin

# Register your models here.
from .models import Game, UserLibrary, GameStatus, GameRating, RatingCategory, RatingType 
#admin.site.register(Game)
admin.site.register(GameRating)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name", "developer", "publisher")
    
admin.site.register(GameStatus)
admin.site.register(UserLibrary)   
admin.site.register(RatingCategory)
admin.site.register(RatingType) 
    
    