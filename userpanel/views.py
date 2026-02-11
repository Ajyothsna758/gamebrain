from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import UserPreference
from games.models import Genre, Platform, PlayerPerspective, Theme
 
def signup_view(request):
    if request.method=="POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user) # for auto login
            # messages.success(request, "Account created successfully")
            return redirect("onboarding")
    else:
        form= SignUpForm()
    return render(request, "user/signup.html", {"form":form})        
     
def homelogin_view(request):
    if request.method=="POST":
        form= LoginForm(request, data=request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect("games")
        else:
            messages.error(request, "Invalid Username or Password")
    else:
        form= LoginForm(request)
    return render(request, "user/home.html", {"form":form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("home")


   
# on-boarding form after signup
@login_required()  
def onboarding_preferences(request):
    prefer, _ = UserPreference.objects.get_or_create(user= request.user)
    if request.method == "POST":
        if "skip" in request.POST:
            prefer.completed_onboarding = True 
            prefer.save()
            return redirect("recommendations:recommendation")
        prefer.preferred_genres.set(request.POST.getlist("genres")) 
        prefer.preferred_platform.set(request.POST.getlist("platforms")) 
        prefer.preferred_player_perspective.set(request.POST.getlist("player_perspectives")) 
        prefer.preferred_themes.set(request.POST.getlist("themes"))
        prefer.completed_onboarding = True
        prefer.save()
        return redirect("recommendations:recommendation")
    return render(request, "user/onboarding_preferences.html",{
        "genres": Genre.objects.all(),
        "platforms": Platform.objects.all(),
        "player_perspectives": PlayerPerspective.objects.all(),
        "themes": Theme.objects.all()
    })      
            