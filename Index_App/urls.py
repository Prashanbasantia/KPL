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
from django.contrib import admin
from django.urls import path
from Index_App import views

urlpatterns = [
    path('', views.home,name="home"),
    path('login/', views.login,name="login"),
    path('matches/', views.matches,name="matches"),
    path('schedule/', views.schedule,name="schedule"),
    path('points/', views.point_table,name="points"),
    path('players/', views.players,name="players"),
    path('live/', views.match_live,name="match_live"),
    path('scorecard/', views.live_scorecard,name="live_scorecard"),
    path('fetch_user_livematch_home/', views.fetch_user_livematch_home,name="fetch_user_livematch_home"),
    path('ajax_live_match/', views.ajax_live_match,name="ajax_live_match"),
]
