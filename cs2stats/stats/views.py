from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from .models import Player, Match, Stat, Team, Series, Map, Round
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
    player = Player.objects.get(user=user)
    teams = Team.objects.filter(players=player)

    
    recent_series = Series.objects.prefetch_related('matches').order_by('-id')[:10]
    
    context = {
        'user': request.user,
        'teams': teams,
        'recent_series': recent_series,
    }

    return render(request, 'stats/dashboard.html', context)



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

# getting data into d3 - https://stackoverflow.com/questions/26453916/passing-data-from-django-to-d3
def d3_round(request):
    round = Round.objects.get(id=35).ticks
    return JsonResponse(round, safe=False)


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    #https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    

    series = Series.objects.filter(Q(team_a=team) | Q(team_b=team))

    return render(request, 'stats/team_detail.html', {
        'team': team,
        'series': series
    })


def series_detail(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    

    if series.team_a is None or series.team_b is None:
        return HttpResponse("One or both teams are not set for this series.", status=400)

    matches = []
    team_wins = {series.team_a.id: 0, series.team_b.id: 0} 

    for match in series.matches.all():
        team_a_wins = match.round_set.filter(winningTeam=match.team_a).count()
        team_b_wins = match.round_set.filter(winningTeam=match.team_b).count()
        winner = match.team_a if team_a_wins > team_b_wins else match.team_b
        matches.append({
            'match': match,
            'team_a_wins': team_a_wins,
            'team_b_wins': team_b_wins,
            'winner': winner
        })

        if team_a_wins > team_b_wins:
            team_wins[series.team_a.id] += 1
        else:
            team_wins[series.team_b.id] += 1

 
    series_winner_id = max(team_wins, key=team_wins.get)
    series_winner = Team.objects.get(id=series_winner_id)

   
    series.winning_team = series_winner
    series.save()

    return render(request, 'stats/series_detail.html', {
        'series': series,
        'matches': matches,
        'series_winner': series_winner
    })

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    team_a_players = match.team_a.players.all()
    team_b_players = match.team_b.players.all()

    
    team_a_stats = match.stat_set.filter(player__in=team_a_players).order_by('-adr')
    team_b_stats = match.stat_set.filter(player__in=team_b_players).order_by('-adr')

    #https://www.w3schools.com/python/python_dictionaries.asp
    #TO DO - put this in db
    round_end_reasons = {
        1: "Bomb detonation",
        7: "Bomb defused",
        8: "T Elimination",
        9: "CT Elimination",
        12: "TimeOut",
        
        
    }
    context = {
        'match': match,
        'rounds': match.round_set.all(),
        'team_a_stats': team_a_stats,
        'team_b_stats': team_b_stats,
        'round_end_reasons': round_end_reasons,

    }
    
    return render(request, 'stats/match_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Player', 'Coach'])
def team_comms(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        raise PermissionDenied("You are not authorized to view this team.")
    
    
    if player not in team.players.all():
        raise PermissionDenied("You are not authorized to view this team.")
    
    return render(request, 'stats/team_comms.html', {'team': team})

    

def teams(request):
    teams = Team.objects.all()
    return render(request, 'stats/teams.html', {'teams': teams})


def player_detail(request, player_id):
    player = get_object_or_404(Player, steam_id=player_id)
    team = get_object_or_404(Team, players=player_id)
    recent_stats = Stat.objects.filter(player=player).order_by('-match__date')[:5]


    return render(request, 'stats/player_detail.html', {
        'player': player,
        'team': team,
        'recent_stats': recent_stats,
        
    })




