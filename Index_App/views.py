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
from django.db.models import Q
import sys
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
    if not schedule:
        schedule = Schedule.objects.filter(status = "Complete").order_by('-schedule_date').first()
    matchinfo = MatchInfo.objects.get(schedule = schedule.id)
    context={
        "schedule_obj":schedule,"matchinfo":matchinfo
    }
    return render(request,'Index_App/index.html',context)
def players(request):
    all_players = Players.objects.all().order_by('-bat_runs','-bowl_wicket')
    context={
        "all_players":all_players
    }
    return render(request,'Index_App/players.html',context)
def matches(request):
    match_info = MatchInfo.objects.all().order_by('-created_at')
    return render(request,'Index_App/review.html',{"match_info":match_info})
def schedule(request):
    teams = Teams.objects.all().order_by('name')
    all_schedules = Schedule.objects.all().order_by('-schedule_date')
    context={
        "all_teams":teams,"all_schedules":all_schedules
    }
    return render(request,'Index_App/schedule.html',context)
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


def match_live(request):
    schedule = Schedule.objects.filter(schedule_date__date = datetime.now().date()).first()
    matchinfo = MatchInfo.objects.get(schedule = schedule.id)
    context={
        "schedule":schedule,"matchinfo":matchinfo
    }
    return render(request,'Index_App/match_live.html',context)

def live_scorecard(request):
    schedule = Schedule.objects.filter(schedule_date__date = datetime.now().date()).first()
    matchinfo = MatchInfo.objects.get(schedule = schedule.id)
    context={
        "schedule":schedule,"matchinfo":matchinfo
    }
    return render(request,'Index_App/live_score_card.html',context)

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_live_match(request):
    try:
        match_info_id = request.GET.get('match_info')
        match_info = MatchInfo.objects.get(id = match_info_id)
        if not match_info.first_ins_complete:
            batters  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",is_bat_inn_one = True)[:2]
            bowlers  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling",is_bowl_inn_one = True)[:1]
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))

            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
        else:
            batters  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",is_bat_inn_two = True)[:2]
            bowlers  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling",is_bowl_inn_two = True)[:1]
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
        data={
        "message":"success",
        "status":True,
        "batters":BatScoreSerializer(batters,many=True).data,
        "bowlers":BowlScoreSerializer(bowlers,many=True).data,

        "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
        "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
        "matchinfo":MatchinfoSerializer(match_info).data,
        "over_details":[]
        }
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        data={
            "message":e,
            "status":False,
            }
        return Response(data,status=status.HTTP_200_OK)
