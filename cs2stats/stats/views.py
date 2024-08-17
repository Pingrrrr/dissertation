from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Player, Match, Stat, Team, Series, Map
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied


def index(request):
    teams = Team.objects.all()
    return render(request, 'stats/index.html', {'teams': teams})

def stratPage(request):
    maps = Map.objects.all()
    return render(request, 'stats/stratPage.html', {'maps':maps})


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
    return render(request, 'stats/match_detail.html', {'match': match, 'rounds': match.round_set.all(), 'stats':match.stat_set.all().order_by('-adr')})



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


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Username or password is incorrect')
            
    return render(request, 'stats/login_register.html')

def signupPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


