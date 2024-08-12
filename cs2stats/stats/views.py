from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Player, Match, Stat, Team
from django.contrib.auth.forms import UserCreationForm




def index(request):
    teams = Team.objects.all()
    return render(request, 'stats/index.html', {'teams': teams})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'stats/team_detail.html', {'team': team})

def team_comms(request):
    return render(request, 'stats/teamComms.html', {})

def teams(request):
    teams = Team.objects.all()
    return render(request, 'stats/teams.html', {'teams': teams})


def player_detail(request, player_id):
    player = get_object_or_404(Player, user_id=player_id)
    team = get_object_or_404(Team, players=player_id)

    return render(request, 'stats/player_detail.html', {
        'player': player,
        'team': team
    })


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index page after successful login
        else:
            messages.error(request, 'Username or password is incorrect')
            
    return render(request, 'stats/login_register.html')

def signupPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to index page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


