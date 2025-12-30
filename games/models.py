from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import FileExtensionValidator

# Create your models here.   
    
class Game(models.Model):
    name= models.CharField(max_length=255)
    developer= models.CharField(max_length=255)
    publisher= models.CharField(max_length=255)
    image= models.ImageField(upload_to="games/")
    main_story= models.DecimalField(max_digits=5, decimal_places=2, null= True)
    main_sides= models.DecimalField(max_digits=5, decimal_places=2, null=True)
    completion= models.DecimalField(max_digits=5, decimal_places=2, null=True)
    description=models.TextField(blank=True)
    released= models.DateField(auto_now=False)
    #rating   
    def average_rating(self):
        avg= self.ratings.aggregate(avg=Avg("rating"))["avg"]
        return round(avg,1) if avg else 0
    def category_average(self, category_key):
        avg= self.ratings.filter(category__key=category_key).aggregate(avg=Avg("rating_type__weight"))["avg"]
        return round(avg,1) if avg else 0
    
    def average_label(self):
        avg= self.average_rating()
        if avg>= 3.5:
            return "Excellent"
        elif avg>= 2.5:
            return "Recommended"
        elif avg>= 1.5:
            return "Average"
        else:
            return "Skip"
    
    
    def __str__(self):
        return self.name

# Ratings
# categories (visual, gameplay, audio, story etc...)
class RatingCategory(models.Model):
    name=models.CharField(max_length=255)
    key=models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
# rating types
class RatingType(models.Model):
    name= models.CharField(max_length=50)
    image= models.FileField(upload_to="ratings/", validators=[FileExtensionValidator(["svg"])])
    weight=models.PositiveSmallIntegerField()
    color=models.CharField(max_length=20, default="#000000")
    class Meta:
        ordering=["-weight"]
        
    def __str__(self):
        return self.name    
# user ratings
class GameRating(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    game=models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    category=models.ForeignKey(RatingCategory, on_delete=models.CASCADE)
    rating_type= models.ForeignKey(RatingType, on_delete=models.CASCADE)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=["game", "user", "category"]
    
    def __str__(self):
        return f"{self.user}: {self.game}-> {self.rating_type}"    
            


# wishlist    
class WishList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    game= models.ForeignKey(Game, on_delete=models.CASCADE)  
    added= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=("user", "game")  
    def __str__(self):
        return f"{self.user}: {self.game}"    

# MyLibrary    
class GameStatus(models.Model):
    name= models.CharField(max_length=255)
    description= models.TextField()
    image= models.FileField(upload_to="status_icons/", validators=[FileExtensionValidator(["svg"])])
    def __str__(self):
        return self.name
    
    
class UserLibrary(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE) 
    game= models.ForeignKey(Game, on_delete=models.CASCADE)
    status=models.ForeignKey(GameStatus, on_delete=models.SET_NULL, null=True)
    added= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=["user", "game"]   
        
    def __str__(self):
        return f"{self.user}: {self.game}"
     
     
                