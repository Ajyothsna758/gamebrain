from django.db import models
from django.contrib.auth.models import User
from games.models import Genre, Platform, PlayerPerspective, Theme

# Create your models here.

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_genres = models.ManyToManyField(Genre, blank= True)
    preferred_platform = models.ManyToManyField(Platform, blank=True)
    preferred_player_perspective = models.ManyToManyField(PlayerPerspective, blank= True)
    preferred_themes = models.ManyToManyField(Theme, blank=True)
    completed_onboarding= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    