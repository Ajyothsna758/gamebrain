from django.urls import path
from . import views

urlpatterns=[
    path("games/", views.games_list, name="games"),
    path("wishlist/toggle/<int:game_id>", views.toggle_wishlist, name="wishlist_toggle"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("library/toggle/<int:game_id>/", views.toggle_library, name="library_toggle"),
    path("update-status/<int:game_id>/<int:status_id>/", views.update_library_status, name="update_status"),
    path("library/", views.library, name="library"),
    path("library/status/<int:status_id>/", views.library, name="library_by_status"),
    
]