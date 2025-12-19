from django.contrib import admin

# Register your models here.
from .models import Game, UserGameRating
#admin.site.register(Game)
admin.site.register(UserGameRating)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name", "developer", "publisher")