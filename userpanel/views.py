from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
 
def signup_view(request):
    if request.method=="POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user) # for auto login
            # messages.success(request, "Account created successfully")
            return redirect("games")
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

@login_required
def games(request):
    return render(request, "games/games.html")            
            