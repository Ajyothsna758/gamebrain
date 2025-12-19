from django.urls import path
from . import views

urlpatterns=[
    path("", views.homelogin_view, name="home"),
    path("sign-up/", views.signup_view, name="sign_up"),
    path("logout", views.logout_view, name="logout"),
]