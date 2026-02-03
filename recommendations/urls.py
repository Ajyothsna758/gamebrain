from django.urls import path
from .views import NewUserGameRecommendationAPIView

app_name = "recommendations"
urlpatterns=[
    path("api/recommendations/cold-start/", NewUserGameRecommendationAPIView.as_view(), name="cold-start"),
]