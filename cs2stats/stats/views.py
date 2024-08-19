from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Player, Match, Stat, Team, Series, Map
from .forms import CreateUserForm, CreateTeamForm
from .decorators import unauthenicated_user, allowed_users

from django.contrib.auth.decorators import login_required

def index(request):
    teams = Team.objects.all()
    return render(request, 'stats/index.html', {'teams': teams})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

@unauthenicated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'Username or password is incorrect')
            
    return render(request, 'stats/login_register.html')

# https://www.youtube.com/watch?v=tUqUdu0Sjyc&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=14
@unauthenicated_user
def signupPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            
            
            user = authenticate(request, username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CreateUserForm()
        
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Player', 'Coach'])
def dashboard(request):
    
    user = request.user
    player =Player.objects.get(user=user)
    team = Team.objects.filter(players=player)
    

    return render(request, 'stats/dashboard.html', {'teams':team})


def create_team(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_detail')
    else:
        form = CreateTeamForm()
    return render(request, 'stats/create_team.html', {'form': form})

def stratPage(request):
    maps = Map.objects.all()
    return render(request, 'stats/stratPage.html', {'maps':maps})

def d3(request):
    maps = Map.objects.all()
    return render(request, 'stats/d3_test.html', {'maps':maps})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    #https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    matches = Match.objects.filter(Q(team_a = team) | Q(team_b = team))
    series = Series.objects.filter(id__in=matches.values_list('series_id'))
    return render(request, 'stats/team_detail.html', {'team': team, 'matches': matches, 'series':series})

def series_detail(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    matches=[]
    for match in series.match_set.all():
        team_a_wins = match.round_set.filter(winningTeam=match.team_a).count()
        team_b_wins = match.round_set.filter(winningTeam=match.team_b).count()
        winner = match.team_a if team_a_wins>team_b_wins else  match.team_b
        matches.append({'match':match, 'team_a_wins':team_a_wins, 'team_b_wins':team_b_wins, 'winner':winner})

    return render(request, 'stats/series_detail.html', {'series': series, 'matches': matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    team_a_players = match.team_a.players.all()
    team_b_players = match.team_b.players.all()

    
    team_a_stats = match.stat_set.filter(player__in=team_a_players).order_by('-adr')
    team_b_stats = match.stat_set.filter(player__in=team_b_players).order_by('-adr')

    context = {
        'match': match,
        'rounds': match.round_set.all(),
        'team_a_stats': team_a_stats,
        'team_b_stats': team_b_stats,
    }
    
    return render(request, 'stats/match_detail.html', context)




def team_comms(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        raise PermissionDenied("You are not authorized to view this team.")
    if player not in team.players.all():
        raise PermissionDenied("You are not authorized to view this team.")
    return render(request, 'teamComms.html', {'team': team})
    

def teams(request):
    teams = Team.objects.all()
    return render(request, 'stats/teams.html', {'teams': teams})


def player_detail(request, player_id):
    player = get_object_or_404(Player, steam_id=player_id)
    team = get_object_or_404(Team, players=player_id)

    return render(request, 'stats/player_detail.html', {
        'player': player,
        'team': team
    })




