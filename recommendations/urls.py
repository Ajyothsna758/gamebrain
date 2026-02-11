from django.urls import path
from . import views

app_name = "recommendations"
urlpatterns=[
    path("recommendations/", views.GameRecommendationAPIView.as_view(), name="recommendation"),
    path("api/recommendations/", views.ExistingUserRecommendationsAPIView.as_view(), name="recommended")
]