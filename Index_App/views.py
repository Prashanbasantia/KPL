from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import  login as log_in
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from Admin_App.serializers import *
def authenticate(username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username ",username)
        user=authenticate(username=username,password=password)
        if user != None:
            if user.is_superuser:
                log_in(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request,"Some Reason You Can't Login")
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request,"Invalid Email or Password")
            return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.is_authenticated and request.user.is_superuser:
            return HttpResponseRedirect(reverse('dashboard'))
        return render(request,'Admin_App/login.html')

def home(request):
    schedule = Schedule.objects.filter(schedule_date__date = datetime.now().date()).first()
    print("schelude",schedule)
    matchinfo = MatchInfo.objects.get(schedule = schedule.id)
    context={
        "schedule":schedule,"matchinfo":matchinfo
    }
    return render(request,'Index_App/index.html',context)
def players(request):
    all_players = Players.objects.all().order_by('name')
    context={
        "all_players":all_players
    }
    return render(request,'Index_App/players.html',context)
def review(request):
    return render(request,'Index_App/review.html')
def schedule(request):
    return render(request,'Index_App/schedule.html')
def point_table(request):
    point_table = PointTable.objects.all().order_by('point')
    context={
        "point_table":point_table
    }
    return render(request,'Index_App/point_table.html',context)

@api_view(['GET'])
@permission_classes([AllowAny],)
def fetch_user_livematch_home(request):
    match_info_id = request.GET.get('match_info')
    match_info = MatchInfo.objects.get(id = match_info_id)
    data={
    "message":"success",
    "status":True,
    "matchinfo":MatchinfoSerializer(match_info).data
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def user_livematch(request):
    match_info_id = request.GET.get('match_info')
    match_info = MatchInfo.objects.get(id = match_info_id)

    batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting")[:2]
    player = Players.objects.filter(id__in=batter.values('player'))

    bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling")[:1]
    player_bowl = Players.objects.filter(id__in=bowler.values('player'))

    score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
    bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))

    playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
    playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))

    squardA = PlayerScore.objects.filter(player__in = playingsquardA.values('player'))
    squardB = PlayerScore.objects.filter(player__in = playingsquardB.values('player'))
    data={
    "message":"success",
    "status":True,
    "players":PlayerImageSerializer(player,many=True).data,
    "score":BatScoreSerializer(score,many=True).data,

    "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
    "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

    "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
    "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
    "matchinfo":MatchinfoSerializer(match_info).data
    }
    return Response(data,status=status.HTTP_200_OK)