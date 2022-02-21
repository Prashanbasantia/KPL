"""Core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Admin_App import views
urlpatterns = [
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('teams/', views.view_teams, name="view_teams"),
    path('team/<str:id>', views.team_details, name="team_details"),
    path('players/', views.view_players, name="view_players"),
    path('player/<str:id>', views.player_details, name="player_details"),
    path('schedules/', views.view_schedules, name="view_schedules"),
    path('schedule/<str:id>', views.schedule_details, name="schedule_details"),
    path('update_squard/<str:id>', views.update_squard, name="update_squard"),
    path('go_live/<str:id>', views.go_live, name="go_live"),
    path('matchinfo', views.matchinfo, name="matchinfo"),
    path('livematch_details/<str:id>', views.livematch_details, name="livematch_details"),
    path('loading_livematch', views.loading_livematch, name="loading_livematch"),
    path('fetch_batters', views.fetch_batters, name="fetch_batters"),
    path('fetch_bowlers', views.fetch_bowlers, name="fetch_bowlers"),
    path('ajax_add_batter', views.ajax_add_batter, name="ajax_add_batter"),
    path('ajax_add_bowler', views.ajax_add_bowler, name="ajax_add_bowler"),
    path('ajax_update_live_runs', views.ajax_update_live_runs, name="ajax_update_live_runs"),

]
