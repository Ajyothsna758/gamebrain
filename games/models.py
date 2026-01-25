from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.validators import FileExtensionValidator

# Create your models here.   

# IGDB Reference models:
class Genre(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)  
    slug = models.SlugField(max_length=255) 
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"

class GameMode(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"  

class Platform(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    alternative_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}" 

class Franchise(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}" 

class PlayerPerspective(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"  
    
class Theme(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"   

class Keyword(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"    
    
class Collection(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}"   

class Company(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    igdb_updated_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.name}: {self.igdb_id}" 
                          
    
# Game Model    
class Game(models.Model):
    igdb_id = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    #image= models.ImageField(upload_to="games/")
    description = models.TextField(blank=True)
    released = models.DateField(null=True, blank=True)
    igdb_updated_at = models.DateTimeField(blank=True, null=True)
    cover_url = models.URLField(null=True, blank=True,)
    story_line = models.TextField(null=True, blank=True)
    hypes = models.IntegerField(null=True, blank=True)
    igdb_rating = models.FloatField(null=True, blank=True)
    igdb_rating_count = models.IntegerField(null=True, blank=True)
    total_rating = models.FloatField(null=True, blank=True)
    total_rating_count = models.IntegerField(null=True, blank=True)
    igdb_url = models.URLField(null=True, blank=True)
    #ref fields
    genres = models.ManyToManyField(Genre, related_name="games", blank=True)
    game_modes = models.ManyToManyField(GameMode, related_name="games", blank=True)
    platforms = models.ManyToManyField(Platform, related_name="games", blank=True)
    franchises = models.ManyToManyField(Franchise, related_name="games", blank=True)
    player_perspectives = models.ManyToManyField(PlayerPerspective, related_name="games", blank=True)
    themes = models.ManyToManyField(Theme, related_name="games", blank=True)
    keywords = models.ManyToManyField(Keyword, related_name="games", blank=True)
    collections = models.ManyToManyField(Collection, related_name="games", blank=True)
    developer = models.ManyToManyField(Company, related_name="developed_games", blank=True)
    publisher = models.ManyToManyField(Company, related_name="published_games", blank=True)
    similar_games = models.ManyToManyField('self', null=True, blank=True)
       
    #rating   
    def overall_average(self):
        avg = self.overall_ratings.aggregate(avg=Avg("rating_type__weight"))["avg"]
        return round(avg,1) if avg else 0
    
    def overall_breakdown(self):
        if not self.overall_ratings.exists():
            return [
                {
                    "id": None,
                    "name": "No Reviews",
                    "image": None,
                    "color": "grey",
                    "count": 0,
                    "percentage": 100.0  
                }
            ]
        
        total = self.overall_ratings.count() or 1
        ratings = RatingType.objects.annotate(
            count = Count("overall_ratings", filter=models.Q(overall_ratings__game=self))
        ).order_by("-weight")
        return [
            {
                "id":r.id,
                "name":r.name,
                "image":r.image.url,
                "color":r.color,
                "count":r.count,
                "percentage":round((r.count / total)*100, 1)
            }
            for r in ratings
        ]
    
    def overall_label(self):
        avg = self.overall_average()
        if avg >= 3.5:
            return "Excellent"
        elif avg >= 2.5:
            return "Recommended"
        elif avg >= 1.5:
            return "Average"
        return "Skip"
    
    def overall_rating_image(self):
        if not self.overall_ratings.exists():
            return None
        avg= self.overall_average()
        if avg >= 3.5:
            rating_type = RatingType.objects.filter(weight__gte=avg).order_by("weight").first()
        elif avg >= 2.5:
            rating_type = RatingType.objects.filter(weight__gte=avg).order_by("weight").first()
        elif avg >= 1.5:
            rating_type = RatingType.objects.filter(weight__gte=avg).order_by("weight").first()
        else:
            rating_type = RatingType.objects.filter(weight__gte=avg).order_by("weight").first()
        return rating_type.image.url if rating_type else None               
        
    def category_average(self, category_key):
        avg = self.category_ratings.filter(category__key=category_key).aggregate(avg=Avg("rating_type__weight"))["avg"]
        return round(avg,1) if avg else 0    
    
    def category_breakdown(self, category):
        total = self.category_ratings.filter(category=category).count() or 1
        ratings = RatingType.objects.annotate(
            count = Count("category_ratings", filter=models.Q(category_ratings__game=self, category_ratings__category=category))
        ).order_by("-weight")
        return [
            {
                "id": r.id,
                "name": r.name,
                "image":r.image.url,
                "color": r.color,
                "count": r.count,
                "category_rating_name": r.category_rating_name,
                "category_rating_description": r.category_rating_description,
                "percent": round((r.count/total)*100,1),
            }
            for r in ratings
        ]
        
    def __str__(self):
        return self.name
    
# time to beat
class GameTimeToBeat(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name="time_to_beat")
    main_story = models.DecimalField(max_digits=5, decimal_places=2, null= True, blank=True)
    main_sides = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 
    def __str__(self):
        return f"{self.game.name}"
# Ratings
# categories (visual, gameplay, audio, story etc...)
class RatingCategory(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
# rating types
class RatingType(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to="ratings/", validators=[FileExtensionValidator(["svg"])])
    weight = models.PositiveSmallIntegerField(default=0)
    color = models.CharField(max_length=20, default="#000000")
    category_rating_name = models.CharField(max_length=50, null=True)
    category_rating_description = models.TextField(max_length=500, null=True)
    class Meta:
        ordering=["-weight"]
        
    def __str__(self):
        return self.name  

# user ratings
class GameOverallRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="overall_ratings")
    rating_type = models.ForeignKey(RatingType, on_delete=models.CASCADE, related_name="overall_ratings")
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=["game", "user"]
    
    def __str__(self):
        return f"{self.user}: {self.game}-> {self.rating_type}"    
            
class GameCategoryRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="category_ratings")
    category = models.ForeignKey(RatingCategory, on_delete=models.CASCADE)
    rating_type = models.ForeignKey(RatingType, on_delete=models.CASCADE, related_name="category_ratings")
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ["game", "user", "category"]  
    def __str__(self):
        return f"{self.user}:{self.game}->{self.category}"              

# wishlist    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  
    added = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "game")  
    def __str__(self):
        return f"{self.user}: {self.game}"    

# MyLibrary    
class GameStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    image = models.FileField(upload_to="status_icons/", validators=[FileExtensionValidator(["svg"])])
    def __str__(self):
        return self.name
    
    
class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.ForeignKey(GameStatus, on_delete=models.SET_NULL, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ["user", "game"]   
        
    def __str__(self):
        return f"{self.user}: {self.game}"
       
# IGDB sync check
class IGDBSyncStatus(models.Model):
    last_updated_at = models.DateTimeField(null=True, blank=True)  
    last_updated_ids = models.JSONField(default=dict, blank=True)   
    

          
                   