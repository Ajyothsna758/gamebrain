from django.contrib import admin

# Register your models here.
from .models import Game, UserGameRating, UserLibrary, GameStatus
#admin.site.register(Game)
admin.site.register(UserGameRating)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name", "developer", "publisher")
    
admin.site.register(GameStatus)
admin.site.register(UserLibrary)    
    
    