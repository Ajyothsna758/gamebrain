from django.urls import path
from . import views

urlpatterns=[
    path("login/", views.homelogin_view, name="login"),
    path("sign-up/", views.signup_view, name="sign_up"),
    path("logout", views.logout_view, name="logout"),
    path("onboarding/", views.onboarding_preferences, name="onboarding"),
]