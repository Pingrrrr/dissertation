from django.urls import path
from . import views
from .views import logout
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('player/<str:player_id>/', views.player_detail, name='player_detail'), 

    path('series/<int:series_id>/', views.series_detail, name='series_detail'), 
    path('series/<int:series_id>/edit/', views.series_edit, name='series_edit'), 


    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('match/<int:match_id>/kills', views.match_kills, name='match_kills'),
    path('match/<int:match_id>/bombs', views.match_bombs, name='match_bombs'),
    path('match/<int:match_id>/rounds', views.match_rounds, name='match_rounds'),

    path('team_comms/<int:team_id>/', views.team_comms, name='team_comms'),
    path('teams/', views.teams, name='teams'),
    
    path('d3/', views.d3, name='d3'),
    path('d3/round/', views.d3_round, name='d3_round'),
    path('create-team/', views.create_team, name='create_team'),
    path('round/<int:round_id>/', views.round_view, name='round_view'),
    path('round/ticks/<int:round_id>/', views.round_ticks, name='round_ticks'),
    path('round/kills/<int:round_id>/', views.kills, name='kills'),

    path('stratPage/', views.stratPage, name='stratPage'),  
    path('strategies/', views.strategies, name='strategies'),
    path('create_strategy/', views.create_strategy, name='create_strategy'),
    path('strategy/addStrategy/', views.add_strategy, name='add_strategy'),
    path('strategy/<int:strategy_id>/', views.strategy, name='strategy'),
    path('strategy/<int:strategy_id>/canvas', views.strategy_canvas,  name='strategy_canvas'),

    path('parsedemo/<int:uploaded_file_id>/', views.parsedemo, name='parsedemo'),
    path('demo/<int:uploaded_file_id>', views.demo, name='demo'),
    path('demos/<int:team_id>', views.demos, name='demos'),

    path('notifications/', views.notifications, name='notifications'),
    path('read_notifications/', views.read_notifications, name='read_notifications'),
    path('read_notification/', views.read_notification, name='read_notification'),


   

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)