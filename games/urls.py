from django.urls import path
from . import views

urlpatterns=[
    path("games/", views.games_list, name="games")
]