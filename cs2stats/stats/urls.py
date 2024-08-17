from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('player/<str:player_id>/', views.player_detail, name='player_detail'), 
    path('series/<int:series_id>/', views.series_detail, name='series_detail'), 
    path('match/<int:match_id>/', views.match_detail, name='match_detail'), 
    path('team_comms/<int:team_id>/', views.team_comms, name='team_comms'),
    path('teams/', views.teams, name='teams'),
    path('stratPage/', views.stratPage, name='stratPage'),
]

