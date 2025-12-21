from django.urls import path
from . import views

urlpatterns=[
    path("games/", views.games_list, name="games"),
    path("wishlist/toggle/<int:game_id>", views.toggle_wishlist, name="wishlist_toggle"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("1/", views.check_svg),
]