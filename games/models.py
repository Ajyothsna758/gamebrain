from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Create your models here.
  
    
class Game(models.Model):
    name= models.CharField(max_length=255)
    developer= models.CharField(max_length=255)
    publisher= models.CharField(max_length=255)
    # rating= models.ForeignKey(Rating, on_delete=models.PROTECT)
    image= models.ImageField(upload_to="games/")
    main_story= models.DecimalField(max_digits=5, decimal_places=2, null= True)
    main_sides= models.DecimalField(max_digits=5, decimal_places=2, null=True)
    completion= models.DecimalField(max_digits=5, decimal_places=2, null=True)
    description=models.TextField(blank=True)
    released= models.DateField(auto_now=False)
    def average_rating(self):
        avg= self.ratings.aggregate(avg=Avg("rating"))["avg"]
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

class UserGameRating(models.Model):
    rating_choices=[
        (4, "Excellent"),
        (3, "Recommended"),
        (2, "Average"),
        (1, "Skip"),
    ]
    rating= models.SmallIntegerField(choices=rating_choices)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    game= models.ForeignKey(Game, related_name="ratings", on_delete=models.CASCADE)
    created_time= models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together=["user", "game"]
    def __str__(self):
        return f"{self.user}={self.game.name}:{self.get_rating_display()}"  
    
class WishList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    game= models.ForeignKey(Game, on_delete=models.CASCADE)  
    added= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=("user", "game")  
    def __str__(self):
        return f"{self.user}: {self.game}"    
    
                