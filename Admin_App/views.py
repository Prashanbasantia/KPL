from re import I
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from datetime import datetime
from django.contrib.auth import  logout as log_out
from django.views.decorators.csrf import csrf_exempt
import json,sys
from django.db import  transaction
from Admin_App.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
#@csrf_protect
# Create your views here.

ROLE_CHOICE=["Batsman","Bowler","Allrounder","Batting Allrounder","Bowling Allrounder"]
BATTING_CHOICE=["Right Handed Bat","Left Handed Bat"]
BOWLING_CHOICE=["Right-arm Fast-medium","Left-arm Fast-medium","Right-arm Medium","Right-arm Medium","Right-arm Offbreak","Right-arm Legbreak","Left-arm Offbreak","Left-arm Legbreak"]
LEAGUE_CHOICE=["League","Qualifier","Final"]

def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('home'))
def dashboard(request):
    return render(request,'Admin_App/dashboard.html')
def view_teams(request):
    if request.method =="POST":
        name = request.POST.get('team_name')
        short_name = request.POST.get('team_short_name')
        logo = request.FILES.get('logo')
        if name == "":
            messages.error(request,"Please Enter Team Name")
            return HttpResponseRedirect(reverse('view_teams'))
        if short_name == "":
            messages.error(request,"Please Enter Short Team Name")
            return HttpResponseRedirect(reverse('view_teams'))
        if Teams.objects.filter(name = name).exists():
            messages.error(request,f"Team Name {name} Already Exists")
            return HttpResponseRedirect(reverse('view_teams'))
        if Teams.objects.filter(short_name = short_name).exists():
            messages.error(request,f"Team Short Name {short_name} Already Exists")
            return HttpResponseRedirect(reverse('view_teams'))
        if logo:
            team = Teams.objects.create(name=name,short_name=short_name,season=Seasons.objects.get(year=datetime.now().year),logo=logo)
            PointTable.objects.create(team = team)
        else:
            team = Teams.objects.create(name=name,short_name=short_name,season=Seasons.objects.get(year=datetime.now().year))
            PointTable.objects.create(team = team)
        messages.success(request,f"Team Name {name} Created Successfully")
        return HttpResponseRedirect(reverse('view_teams'))
    else:
        teams = Teams.objects.all().order_by('name')
        context={
            "all_teams":teams
        }
        return render(request,'Admin_App/teams.html',context)
def team_details(request,id):
    if request.method =="POST":
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            address = request.POST.get('address')
            role = request.POST.get('role')
            batting_style = request.POST.get('batting_style')
            bowling_style = request.POST.get('bowling_style')
            image = request.FILES.get('image')
            if name == "":
                messages.error(request,"Please Enter Player Name")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if age == "":
                messages.error(request,"Please Enter Player Age")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if address == "":
                messages.error(request,"Please Enter Player address")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if role == "":
                messages.error(request,"Please Select Player Role")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if batting_style == "":
                messages.error(request,"Please Select Player Batting Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if bowling_style == "":
                messages.error(request,"Please Select Player Bowling Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            
            if role not in ROLE_CHOICE:
                messages.error(request,"Please Select Valid Player Role")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if batting_style not in BATTING_CHOICE:
                messages.error(request,"Please Select Valid Player Batting Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if bowling_style not in BOWLING_CHOICE:
                messages.error(request,"Please Select Valid Player Bowling Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))

            team = Teams.objects.get(id = id)
            if not image:
                Players.objects.create(team = team, name = name, age = age, address = address, role = role, batting_style = batting_style, bowling_style = bowling_style )
            else:
                Players.objects.create(team = team, name = name, age = age, address = address, role = role, batting_style = batting_style, bowling_style = bowling_style,image = image ) 
            messages.success(request,f"Player {name} Created Successfully")
            return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))    
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
    else:
        players = Players.objects.filter(team=id).order_by('name')
        team = Teams.objects.get(id = id)
        context={
            "all_players":players,"team":team
            }
        return render(request,'Admin_App/team_details.html',context)

def view_players(request):
    players = Players.objects.all().order_by('name')
    context={
        "all_players":players
        }
    return render(request,'Admin_App/players.html',context)


def player_details(request,id):
    if request.method =="POST":
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            address = request.POST.get('address')
            role = request.POST.get('role')
            batting_style = request.POST.get('batting_style')
            bowling_style = request.POST.get('bowling_style')
            image = request.FILES.get('image')
            if name == "":
                messages.error(request,"Please Enter Player Name")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if age == "":
                messages.error(request,"Please Enter Player Age")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if address == "":
                messages.error(request,"Please Enter Player address")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if role == "":
                messages.error(request,"Please Select Player Role")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if batting_style == "":
                messages.error(request,"Please Select Player Batting Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if bowling_style == "":
                messages.error(request,"Please Select Player Bowling Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            
            if role not in ROLE_CHOICE:
                messages.error(request,"Please Select Valid Player Role")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if batting_style not in BATTING_CHOICE:
                messages.error(request,"Please Select Valid Player Batting Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
            if bowling_style not in BOWLING_CHOICE:
                messages.error(request,"Please Select Valid Player Bowling Style")
                return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))

            team = Teams.objects.get(id = id)
            if not image:
                Players.objects.create(team = team, name = name, age = age, address = address, role = role, batting_style = batting_style, bowling_style = bowling_style ) 
            else:
                Players.objects.create(team = team, name = name, age = age, address = address, role = role, batting_style = batting_style, bowling_style = bowling_style,image = image ) 

            messages.success(request,f"Player {name} Created Successfully")
            return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))    
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('team_details',kwargs={"id":id}))
    else:
        player = Players.objects.get(id=id)
        context={
            "player":player
            }
        return render(request,'Admin_App/player_details.html',context)

def view_schedules(request):
    if request.method =="POST":
        teamA = request.POST.get('teamA')
        teamB = request.POST.get('teamB')
        match_date = request.POST.get('date')
        match_time = request.POST.get('time')
        match_type = request.POST.get('match_type')
        if match_date == "":
            messages.error(request,"Please Enter Match Date")
            return HttpResponseRedirect(reverse('view_schedules')) 
        if teamA == teamB:
            messages.error(request,"Please Select Diffrent Team")
            return HttpResponseRedirect(reverse('view_schedules'))
        if match_time == "":
            messages.error(request,"Please Enter Match Time")
            return HttpResponseRedirect(reverse('view_schedules'))        
        if teamA == "":
            messages.error(request,"Please Select Team A")
            return HttpResponseRedirect(reverse('view_teams'))
        if teamB == "":
            messages.error(request,"Please Select Team B")
            return HttpResponseRedirect(reverse('view_schedules'))
        if match_type == "":
            messages.error(request,"Please Select Match Type")
            return HttpResponseRedirect(reverse('view_schedules'))
        if match_type not in LEAGUE_CHOICE:
            messages.error(request,"Please Select Valid Match Type")
            return HttpResponseRedirect(reverse('view_schedules'))
        if not Teams.objects.filter(id = teamA).exists():
            messages.error(request,f"Team A Not Exists")
            return HttpResponseRedirect(reverse('view_schedules'))
        if not Teams.objects.filter(id = teamB).exists():
            messages.error(request,f"Team B Not Exists")
            return HttpResponseRedirect(reverse('view_schedules'))
        dt = f"{match_date} {match_time}"
        Schedule.objects.create(match_type = match_type,team_one = Teams.objects.get(id = teamA),team_two = Teams.objects.get(id = teamB),schedule_date = datetime.strptime(dt,"%Y-%m-%d %H:%M"))
        messages.success(request,"Schedule Created Successfully")
        return HttpResponseRedirect(reverse('view_schedules'))
    else:
        teams = Teams.objects.all().order_by('name')
        all_schedules = Schedule.objects.all().order_by('schedule_date')
        context={
            "all_teams":teams,"all_schedules":all_schedules
        }
        return render(request,'Admin_App/schedules.html',context)


def schedule_details(request,id):
    if request.method =="POST":
        try:
            player_id = request.POST.getlist('player_id')
            is_captain = request.POST.get('is_captain')
            team_id = request.POST.get('team_id')
            print("team-id",team_id)
            if player_id == []:
                messages.error(request,"Please Select Player")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
            if not is_captain:
                messages.error(request,"Please Select Catpain")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
            if len(player_id) != 11 :
                messages.error(request,"Please Select 11 Players")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))

            if PlayingSquard.objects.filter(schedule=id,player__in=Players.objects.filter(team = team_id).values('id')).exists():
                messages.error(request,"Squard Already Declared")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
            with transaction.atomic():
                schedule = Schedule.objects.get(id=id)
                for i in player_id:
                    play = Players.objects.get(id=i)
                    PlayingSquard.objects.create(player = play, schedule = schedule, is_play=True)
                    play.match= + 1 
                    play.ins= + 1 
                    play.save()

                pl=PlayingSquard.objects.get(schedule = id ,player=Players.objects.get(id=is_captain))
                pl.is_captain = True
                pl.save()

                for i in Players.objects.filter(team = pl.player.team.id).exclude(id__in=player_id):
                    if not PlayingSquard.objects.filter(player=i.id).exists():
                        PlayingSquard.objects.create(player = i, schedule = schedule)

                messages.success(request,"Playing Squard Created Successfully")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))    
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
    else:
        schedule = Schedule.objects.get(id=id)
        if schedule.status == "Today":
            team_A = Players.objects.filter(team=schedule.team_one)
            team_B = Players.objects.filter(team=schedule.team_two)
            squardA = PlayingSquard.objects.filter(schedule = id,player__in=team_A.values('id')).select_related('schedule')
            squardB = PlayingSquard.objects.filter(schedule = id,player__in=team_B.values('id')).select_related('schedule')
            context={
                "schedule":schedule,"team_A":team_A,"team_B":team_B,"squardA":squardA,"squardB":squardB
                }
            return render(request,'Admin_App/schedule_details.html',context)
        elif schedule.status == "Incomplete":
            messages.error(request,"Can Not Access Up-comming Schedule")
            return HttpResponseRedirect(reverse('view_schedules'))
        else:
            pass


def update_squard(request,id):
    if request.method =="POST":
        try:
            player_id = request.POST.getlist('player_id')
            is_captain = request.POST.get('is_captain')
            team_id = request.POST.get('team_id')
            if player_id == []:
                messages.error(request,"Please Select Player")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
            if not is_captain:
                messages.error(request,"Please Select Catpain")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))            
            if len(player_id) != 11:
                messages.error(request,"Please Select 11 Players")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))

            own_tema_player = Players.objects.filter(team = team_id).values('id')
            print('one  1')
            for i in PlayingSquard.objects.filter(schedule = id,player__in = own_tema_player ):
                if str(i.player.id) in player_id:
                    i.is_play = True
                    i.save()
                else:
                    i.is_play = False
                    i.save()
            print('one  2')
            pl=PlayingSquard.objects.get(schedule = id ,is_captain = True,player__in = own_tema_player )
            if pl:
                if str(pl.player.id) != is_captain:
                    pl.is_captain = False
                    pl.save()
                    newc=PlayingSquard.objects.get(schedule = id ,player =is_captain)
                    newc.is_captain = True
                    newc.save()
            else:
                newc=PlayingSquard.objects.get(schedule = id ,player =is_captain)
                newc.is_captain = True
                newc.save()

            
            messages.success(request,"Playing Squard Updated Successfully")
            return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))    
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            messages.error(request,e)
            return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
    else:
        messages.error(request,"POST Method Required")
        return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))


def go_live(request,id):
    if request.method =="POST":
        try:
            toss_own = request.POST.get('toss_own')
            toss_own_option = request.POST.get('toss_own_option')
            umpire_one = request.POST.get('umpire_one')
            umpire_two = request.POST.get('umpire_two')
            if not toss_own :
                messages.error(request,"Please Select Which team Own The Toss")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
            if not toss_own_option :
                messages.error(request,"Please Select Which Option Take Toss Own Team")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))

            if MatchInfo.objects.filter(schedule = id,is_toss = True).exists():
                messages.error(request,"Your Already in Live ! Go Match Info View Details")
                return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))

            
            with transaction.atomic():
                schedule = Schedule.objects.get(id=id)
                team = Teams.objects.get(id=toss_own)
                if toss_own == schedule.team_one.id:
                    match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_one,second_ins=schedule.team_two,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)
                else:
                    match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_two,second_ins=schedule.team_one,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)

                for i in PlayingSquard.objects.filter(schedule=schedule.id ,is_play = True):
                    if schedule.team_one.id == i.player.team.id:
                        PlayerScore.objects.create(player = i.player,matchinfo=match_info)
                    else:
                        PlayerScore.objects.create(player = i.player,matchinfo=match_info)

                schedule.status = "Live"
                schedule.save()
                messages.success(request,"Hey You Are On Live !")
                return HttpResponseRedirect(reverse('livematch_details',kwargs={"id":match_info.id}))    
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            messages.error(request,e)
            return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
    else:
        messages.error(request,"POST Method Required")
        return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":id}))
def matchinfo(request):
    match_info = MatchInfo.objects.all().order_by('-created_at')
    context={
        "match_info":match_info,
        }
    return render(request,'Admin_App/matchinfo.html',context)

def livematch_details(request,id):
    match_info = MatchInfo.objects.get(id = id)
    schedule = Schedule.objects.get(id = match_info.schedule.id)
    team_A = Players.objects.filter(team=schedule.team_one.id)
    team_B = Players.objects.filter(team=schedule.team_two.id)
    squardA = PlayingSquard.objects.filter(schedule = schedule.id,player__in=team_A.values('id')).select_related('schedule')
    squardB = PlayingSquard.objects.filter(schedule = schedule.id,player__in=team_B.values('id')).select_related('schedule')
    context={
        "schedule":schedule,"team_A":team_A,"team_B":team_B,"squardA":squardA,"squardB":squardB,"match_info":match_info
        }
    return render(request,'Admin_App/livematch_details.html',context)

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def loading_livematch(request):
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def fetch_batters(request):
    try:
        match_info_id = request.GET.get('match_info')
        match_info = MatchInfo.objects.get(id = match_info_id)
        if match_info.first_ins_complete:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Not Batting",player__in = Players.objects.filter(team= match_info.second_ins.id).values('id'))
            player = Players.objects.filter(id__in=batter.values('player')).values('id','name')
            data={
                "message":"success",
                "status":True,
                "objs":PlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)

        else:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Not Batting",player__in = Players.objects.filter(team= match_info.first_ins.id).values('id'))
            player = Players.objects.filter(id__in=batter.values('player')).values('id','name')
            data={
                "message":"success",
                "status":True,
                "objs":PlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        data={
            "message":e,
            "status":False,
            }
        return Response(data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def fetch_bowlers(request):
    try:
        match_info_id = request.GET.get('match_info')
        match_info = MatchInfo.objects.get(id = match_info_id)
        if match_info.first_ins_complete:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = Players.objects.filter(team= match_info.first_ins.id).values('id'),bowl_status = "Not Bowling")
            player = Players.objects.filter(id__in=batter.values('player')).values('id','name')
            data={
                "message":"success",
                "status":True,
                "objs":PlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)
        else:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = Players.objects.filter(team= match_info.second_ins.id).values('id'),bowl_status = "Not Bowling")
            player = Players.objects.filter(id__in=batter.values('player')).values('id','name')
            data={
                "message":"success",
                "status":True,
                "objs":PlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        data={
            "message":e,
            "status":False,
            }
        return Response(data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_add_batter(request):
    try:
        player_id = request.GET.get('player_id')
        is_stricker = request.GET.get('is_stricker')
        match_info_id = request.GET.get('match_info')
        print(player_id,is_stricker,match_info_id)
        player = Players.objects.get(id=player_id)
        match_info = MatchInfo.objects.get(id = match_info_id)
        with transaction.atomic():   
            bat_score = PlayerScore.objects.get(matchinfo = match_info.id,player = player_id)
            bat_score.bat_status = "Batting"       
            if is_stricker == "True":
                for i in PlayerScore.objects.filter(bat_is_striker=True,matchinfo = match_info.id,player__in = Players.objects.filter(team = player.team.id).values('id')):
                    i.is_striker  = False
                    i.save()
                bat_score.bat_is_striker = True
            bat_score.save()
            data={
                "message":"success",
                "status":True,
                "players":PlayerImageSerializer(player).data,
                "score":BatScoreSerializer(bat_score).data
                }      
            return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        data={
            "message":e,
            "status":False,
            }
        return Response(data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_add_bowler(request):
    try:
        player_id = request.GET.get('bowler_id')
        match_info_id = request.GET.get('match_info')
        player = Players.objects.get(id=player_id)
        match_info = MatchInfo.objects.get(id = match_info_id)
        with transaction.atomic():
            bowl_score = PlayerScore.objects.get(matchinfo = match_info.id,player = player_id)
            bowl_score.bowl_status = "Bowling"       
            bowl_score.save()
            data={
                "message":"success",
                "status":True,
                "players":PlayerImageSerializer(player).data,
                "score":BowlScoreSerializer(bowl_score).data
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

def cal_over(no_b):
    b= 6
    for i in range(0,no_b+1):
        if no_b >= b*i and no_b < b*(i+1):
            dec_bal= no_b-b*i
            out_over= f"{i}.{dec_bal}"
            return float(out_over)

def cal_ball(over):
    fnum = str(float(over)).split('.')
    ball = int(fnum[0])*6+int(fnum[1])
    return ball

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_update_live_runs(request):
    try:
        match_info_id = request.GET.get('match_info')
        run = int(request.GET.get('run'))
        match_info = MatchInfo.objects.get(id = match_info_id)
        
        batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting")[:2]
        bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling")[:1]
        with transaction.atomic():
            if batter[0].bat_is_striker:
                stricker= batter[0]
                non_stricker = batter[1]
            else:
                stricker= batter[1]
                non_stricker = batter[0]

            if match_info.first_ins_complete:
                ba = cal_ball(match_info.second_ins_overs)+1
                ov = cal_over(ba)
                match_info.second_ins_runs = match_info.second_ins_runs+run
                match_info.secondins_overs = ov
                match_info.second_ins_crr = round(match_info.second_ins_runs+run/ov,2)
                match_info.save()
            else:
                ba = cal_ball(match_info.first_ins_overs)+1
                ov = cal_over(ba)
                match_info.first_ins_runs = match_info.first_ins_runs+run
                match_info.first_ins_overs = ov
                match_info.first_ins_crr = round(match_info.first_ins_runs+run/ov,2)
                match_info.save()

            if run%2 == 0:
                stricker.bat_runs = stricker.bat_runs+run
                stricker.bat_balls= stricker.bat_balls+1 
                stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                if run == 4 :
                    stricker.bat_fours=stricker.bat_fours+1
                if run == 6:
                    stricker.bat_sixes = stricker.bat_sixes+1
                stricker.save()
            else:
                stricker.bat_runs = stricker.bat_runs+run
                stricker.bat_balls= stricker.bat_balls+1 
                stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                stricker.bat_is_striker = False
                stricker.save()
                non_stricker.bat_is_striker = True
                non_stricker.save()

            bowler__player = bowler[0]
            bba = cal_ball(bowler__player.bowl_over)+1
            bov = cal_over(bba)
            bowler__player.bowl_runs=bowler__player.bowl_runs+run
            bowler__player.bowl_over=bov
            bowler__player.bowl_economy=round(bowler__player.bowl_runs+run/bov,2)
            bowler__player.save()
            #check over end
            is_endball = int(str(float(bov)).split('.')[1])
            if is_endball == 0:
                if run%2 == 0:
                    stricker.bat_is_striker = False
                    stricker.save()
                    non_stricker.bat_is_striker = True
                    non_stricker.save()
                bowler__player.bowl_status="Recent"
                bowler__player.save()
                recent_bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status = "Recent")[:1]
                if recent_bowler[0]:
                    recent_bowler[0].bowl_status = "Not Bowling"
                    recent_bowler[0].save()
                    print("recenet change")
            player = Players.objects.filter(id__in=batter.values('player'))
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



