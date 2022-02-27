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
from django.db.models import Q
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
            if len(player_id) >= 11 :
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
                    #play.ins= + 1 
                    play.save()

                pl=PlayingSquard.objects.get(schedule = id ,player=Players.objects.get(id=is_captain),is_play=True)
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
            print(toss_own_option,toss_own)
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
                if toss_own == str(schedule.team_one.id):
                    print("team",schedule.team_one.name,schedule.team_one.id)
                    if toss_own_option == "Elected To Bat First":
                        print("elect bal first")
                        match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_one,second_ins=schedule.team_two,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)
                    else:
                        print("elected to bolw first")
                        match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_two,second_ins=schedule.team_one,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)
                    
                else:
                    print("team 2",schedule.team_two.name,schedule.team_two.id)
                    if toss_own_option == "Elected To Bat First":
                        print("elect bal first")
                        match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_two,second_ins=schedule.team_one,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)
                    else:
                        print("elected to bolw first")
                        match_info = MatchInfo.objects.create(schedule = schedule,is_toss = True,first_ins=schedule.team_one,second_ins=schedule.team_two,umpire_one = umpire_one,umpire_two = umpire_two,toss_own=team.name,toss_own_options = toss_own_option)

                    

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
    try:
        match_info = MatchInfo.objects.get(id = id)
        schedule = Schedule.objects.get(id=match_info.schedule.id)
        context={
        "match_info":match_info
            }
        if schedule.status == "Live":
            return render(request,'Admin_App/livematch_details.html',context)
        elif schedule.status == "Complete":
            return render(request,'Admin_App/reviewmatch_details.html',context)
        else:
            return HttpResponseRedirect(reverse('matchinfo'))

    except Exception as e:
        print(e )
        return HttpResponseRedirect(reverse('matchinfo')) 

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def loading_livematch(request):
    try:
        match_info_id = request.GET.get('match_info')
        match_info = MatchInfo.objects.get(id = match_info_id)
        if not match_info.first_ins_complete:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",is_bat_inn_one = True)[:2]
            player = Players.objects.filter(id__in=batter.values('player'))

            bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling",is_bowl_inn_one = True)[:1]
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))

            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))

            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))

            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
        else:
            batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",is_bat_inn_two = True)[:2]
            player = Players.objects.filter(id__in=batter.values('player'))

            bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling",is_bowl_inn_two = True)[:1]
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))

            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))

            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))

            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')

        if bowler:
            over_details = OverDetails.objects.filter(matchinfo = match_info_id,player = bowler[0].player.id).order_by('created_at')
            over_details_serializer = OverDetailsSerializer(over_details,many=True).data
        else:
            over_details_serializer = []

        data={
        "message":"success",
        "status":True,
        "players":PlayerImageSerializer(player,many=True).data,
        "score":BatScoreSerializer(score,many=True).data,

        "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
        "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

        "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
        "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
        "matchinfo":MatchinfoSerializer(match_info).data,
        "over_details":over_details_serializer
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
            player = Players.objects.filter(id__in=batter.values('player'))
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
            batter  = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(player__in = Players.objects.filter(team= match_info.first_ins.id).values('id')),Q(bowl_status = "Not Bowling")| Q(bowl_status = "Bowled"))
            player = Players.objects.filter(id__in=batter.values('player')).values('id','name')
            data={
                "message":"success",
                "status":True,
                "objs":PlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)
        else:
            batter  = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(player__in = Players.objects.filter(team= match_info.second_ins.id).values('id')),Q(bowl_status = "Not Bowling")| Q(bowl_status = "Bowled"))
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
        player = Players.objects.get(id=player_id)
        match_info = MatchInfo.objects.get(id = match_info_id)
        with transaction.atomic():   
            bat_score = PlayerScore.objects.get(matchinfo = match_info.id,player = player_id)
            bat_score.bat_status = "Batting" 
            if not  match_info.first_ins_complete:    
                bat_score.is_bat_inn_one = True 
            else:
                bat_score.is_bat_inn_two = True     
            bat_score.updated_at = datetime.now()       
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
            bowl_score.updated_at = datetime.now() 
            if not  match_info.first_ins_complete:    
                bowl_score.is_bowl_inn_one = True 
            else:
                bowl_score.is_bowl_inn_two = True        
            bowl_score.save()
            OverDetails.objects.create(matchinfo=match_info,player=player,over_status = True)
            data={
                "message":"success",
                "status":True,
                "players":PlayerImageSerializer(player).data,
                "score":BowlScoreSerializer(bowl_score).data,
                "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player =player.id).order_by('created_at'),many=True).data
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
                match_info.second_ins_overs = ov
                match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                match_info.save()
            else:
                ba = cal_ball(match_info.first_ins_overs)+1
                ov = cal_over(ba)
                match_info.first_ins_runs = match_info.first_ins_runs+run
                match_info.first_ins_overs = ov
                match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
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
            eco = (bowler__player.bowl_runs+run)/bov
            bowler__player.bowl_runs=bowler__player.bowl_runs+run
            bowler__player.bowl_over=bov
            bowler__player.bowl_economy=round(eco,2)
            bowler__player.save()

            od = OverDetails.objects.filter(over_status = True,matchinfo = match_info_id,player = bowler__player.player.id).order_by('-created_at').first()
            if od.ball_count == 0:
                od.over_runs = od.over_runs + run
                od.ball_count = 1
                od.over_ball_one = run
                od.save()
            elif od.ball_count == 1:
                od.over_runs = od.over_runs + run
                od.ball_count = 2
                od.over_ball_two = run
                od.save()
            elif od.ball_count == 2:
                od.over_runs = od.over_runs + run
                od.ball_count = 3
                od.over_ball_three = run
                od.save()
            elif od.ball_count == 3:
                od.over_runs = od.over_runs + run
                od.ball_count = 4
                od.over_ball_four = run
                od.save()
            elif od.ball_count == 4:
                od.over_runs = od.over_runs + run
                od.ball_count = 5
                od.over_ball_five = run
                od.save()
            elif od.ball_count == 5:
                od.over_runs = od.over_runs + run
                od.ball_count = 6
                od.over_ball_six = run
                od.save()
            elif od.ball_count == 6:
                od.over_status = False
                od.save()
            
            
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
                #recent bowler
                recent_bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status = "Recent").exclude(id = bowler__player.id)
                if recent_bowler.exists():
                    rec_bowl = recent_bowler.first()
                    rec_bowl.bowl_status = "Bowled"
                    rec_bowl.save()

            player = Players.objects.filter(id__in=batter.values('player'))
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))
            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
            data={
            "message":"success",
            "status":True,
            "players":PlayerImageSerializer(player,many=True).data,
            "score":BatScoreSerializer(score,many=True).data,

            "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
            "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

            "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
            "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
            "matchinfo":MatchinfoSerializer(match_info).data,
            "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player = bowler__player.player.id).order_by('created_at'),many=True).data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_update_live_extra_runs(request):
    try:
        match_info_id = request.GET.get('match_info')
        run = int(request.GET.get('run'))
        is_leg_bye = request.GET.get('is_leg_bye')
        print("is leg bye",is_leg_bye)
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
                if  is_leg_bye == "Lbye":
                    ba = cal_ball(match_info.second_ins_overs)+1
                    ov = cal_over(ba)
                    match_info.second_ins_extra_runs = match_info.second_ins_extra_runs+run
                    match_info.second_ins_extra_bye = match_info.second_ins_extra_bye+run
                    match_info.second_ins_overs = ov
                    match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                    match_info.second_ins_runs = match_info.second_ins_runs+run
                    match_info.save()
                else:
                    ba = cal_ball(match_info.second_ins_overs)
                    ov = cal_over(ba)
                    match_info.second_ins_extra_runs = match_info.second_ins_extra_runs+run+1
                    match_info.second_ins_extra_bye = match_info.second_ins_extra_bye+run
                    match_info.second_ins_extra_wd = match_info.second_ins_extra_wd+1
                    match_info.second_ins_overs = ov
                    match_info.second_ins_crr = round((match_info.second_ins_runs+run+1)/ov,2)
                    match_info.second_ins_runs = match_info.second_ins_runs+run
                    match_info.save()
            else:
                if  is_leg_bye == "Lbye":
                    ba = cal_ball(match_info.first_ins_overs)+1
                    ov = cal_over(ba)
                    match_info.first_ins_runs = match_info.first_ins_runs+run
                    match_info.first_ins_extra_runs = match_info.first_ins_extra_runs+run
                    match_info.first_ins_extra_bye = match_info.first_ins_extra_bye+run
                    match_info.first_ins_overs = ov
                    match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
                    match_info.save()
                else:
                    ba = cal_ball(match_info.first_ins_overs)
                    ov = cal_over(ba)
                    match_info.first_ins_runs = match_info.first_ins_runs+run+1
                    match_info.first_ins_extra_runs = match_info.first_ins_extra_runs+run
                    match_info.first_ins_extra_wd = match_info.first_ins_extra_wd+1
                    match_info.first_ins_overs = ov
                    match_info.first_ins_crr = round((match_info.first_ins_runs+run+1)/ov,2)
                    match_info.save()
                

            if run%2 == 0:
                if  is_leg_bye == "Lbye":
                    stricker.bat_balls= stricker.bat_balls+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs)/(stricker.bat_balls+1))*100,2)
                    stricker.save()
                
            else:
                if  is_leg_bye == "Lbye":
                    stricker.bat_balls= stricker.bat_balls+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs)/(stricker.bat_balls+1))*100,2)
                    stricker.save()
                
                stricker.bat_is_striker = False
                stricker.save()
                non_stricker.bat_is_striker = True
                non_stricker.save()
            #bowler update 
            bowler__player = bowler[0]
            od = OverDetails.objects.filter(over_status = True,matchinfo = match_info_id,player = bowler__player.player.id).order_by('-created_at').first()
            if  is_leg_bye == "Lbye":
                if od.ball_count == 0:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 1
                elif od.ball_count == 1:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 2
                elif od.ball_count == 2:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 3
                elif od.ball_count == 3:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 4
                elif od.ball_count == 4:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 5
                elif od.ball_count == 5:
                    od.over_runs = od.over_runs + run
                    od.ball_count = 6
                elif od.ball_count == 6:
                    od.over_status = False
                od.over_run_bye= od.over_run_bye+run
                od.save()

                bba = cal_ball(bowler__player.bowl_over)+1
                bov = cal_over(bba)
                eco = (bowler__player.bowl_runs)/bov
                bowler__player.bowl_over=bov
                bowler__player.bowl_economy=round(eco,2)
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
                    #recent bowler
                    recent_bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status = "Recent").exclude(id = bowler__player.id)
                    if recent_bowler.exists():
                        rec_bowl = recent_bowler.first()
                        rec_bowl.bowl_status = "Not Bowling"
                        rec_bowl.save()

            
            else :
                od.over_run_bye = od.over_run_bye+run
                od.over_run_wd = od.over_run_wd+1
                od.over_runs = od.over_runs+run+1
                od.save()

                bba = cal_ball(bowler__player.bowl_over)
                bov = cal_over(bba)
                if bba == 0:
                    eco = -run
                else:
                    eco = (bowler__player.bowl_runs+1)/bov
                bowler__player.bowl_over=bov
                bowler__player.bowl_economy=round(eco,2)
                bowler__player.save()
           
            player = Players.objects.filter(id__in=batter.values('player'))
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))
            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')

            data={
            "message":"success",
            "status":True,
            "players":PlayerImageSerializer(player,many=True).data,
            "score":BatScoreSerializer(score,many=True).data,

            "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
            "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

            "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
            "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
            "matchinfo":MatchinfoSerializer(match_info).data,
            "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player = bowler__player.player.id).order_by('created_at'),many=True).data

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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_update_live_wd_runs(request):
    try:
        match_info_id = request.GET.get('match_info')
        is_wd = request.GET.get('wd')
        run = 1
        match_info = MatchInfo.objects.get(id = match_info_id)
        batter  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting")[:2]
        bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status ="Bowling")[:1]
        with transaction.atomic():
            if match_info.first_ins_complete:
                ba = cal_ball(match_info.second_ins_overs)
                ov = cal_over(ba)
                print("over",ov)
                match_info.second_ins_runs = match_info.second_ins_runs+run
                match_info.second_ins_extra_runs = match_info.second_ins_extra_runs+run
                match_info.second_ins_overs = ov
                match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                match_info.second_ins_extra_wd = match_info.second_ins_extra_wd+run
                match_info.save()
            else:
                ba = cal_ball(match_info.first_ins_overs)
                ov = cal_over(ba)
                match_info.first_ins_runs = match_info.first_ins_runs+run
                match_info.first_ins_extra_runs = match_info.first_ins_extra_runs+run
                match_info.first_ins_overs = ov
                match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
                match_info.first_ins_extra_wd = match_info.first_ins_extra_wd+run
                match_info.save()

            #bowler update 

            bowler__player = bowler[0]
            bba = cal_ball(bowler__player.bowl_over)
            bov = cal_over(bba)
            if bba == 0:
                eco = -1.00
            else:
                eco = (bowler__player.bowl_runs)/bov
            bowler__player.bowl_runs=bowler__player.bowl_runs+run
            bowler__player.bowl_economy=round(eco,2)
            bowler__player.save()

            od = OverDetails.objects.filter(over_status = True,matchinfo = match_info_id,player = bowler__player.player.id).order_by('-created_at').first()
            if is_wd =="Wd":
                od.over_run_wd = od.over_run_wd+run
            else:
                od.over_run_nb = od.over_run_wd+run
            od.over_runs = od.over_runs+run
            od.save()
            #check over end
            
            player = Players.objects.filter(id__in=batter.values('player'))
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))
            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')

            data={
            "message":"success",
            "status":True,
            "players":PlayerImageSerializer(player,many=True).data,
            "score":BatScoreSerializer(score,many=True).data,

            "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
            "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

            "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
            "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
            "matchinfo":MatchinfoSerializer(match_info).data,
            "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player = bowler__player.player.id).order_by('created_at'),many=True).data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def fetch_wicket_player(request):
    try:
        match_info_id = request.GET.get('match_info')
        match_info = MatchInfo.objects.get(id = match_info_id)
        if match_info.first_ins_complete:
            player  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",player__in = Players.objects.filter(team= match_info.second_ins.id).values('id'))
            data={
                "message":"success",
                "status":True,
                "objs":WicketPlayerSerializer(player,many=True).data
                }
            return Response(data,status=status.HTTP_200_OK)

        else:
            player  = PlayerScore.objects.filter(matchinfo = match_info_id,bat_status ="Batting",player__in = Players.objects.filter(team= match_info.first_ins.id).values('id'))
            data={
                "message":"success",
                "status":True,
                "objs":WicketPlayerSerializer(player,many=True).data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_update_player_wicket(request):
    try:
        match_info_id = request.GET.get('match_info')
        player_score_id = request.GET.get('player_score_id')
        is_run_out = request.GET.get('is_run_out')
        wicket_is_run = request.GET.get('wicket_is_run')
        if wicket_is_run == "True":
            run = int(request.GET.get('wicket_hit_run'))
        else:
            run = int(request.GET.get('wicket_extra_runs'))
            wicket_is_leg_bye = request.GET.get('wicket_is_leg_bye')


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
                if wicket_is_run == "True":
                    ba = cal_ball(match_info.second_ins_overs)+1
                    ov = cal_over(ba)
                    match_info.second_ins_runs = match_info.second_ins_runs+run
                    match_info.second_ins_overs = ov
                    match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                    match_info.second_ins_wkts = match_info.second_ins_wkts+1
                    match_info.save()
                else:
                    if wicket_is_leg_bye == "True":
                        ba = cal_ball(match_info.second_ins_overs)+1
                        ov = cal_over(ba)
                        match_info.second_ins_runs = match_info.second_ins_runs+run
                        match_info.second_ins_overs = ov
                        match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                        match_info.second_ins_wkts = match_info.second_ins_wkts+1
                        match_info.save()
                    else:
                        ba = cal_ball(match_info.second_ins_overs)
                        ov = cal_over(ba)
                        match_info.second_ins_runs = match_info.second_ins_runs+run
                        match_info.second_ins_overs = ov
                        match_info.second_ins_crr = round((match_info.second_ins_runs+run)/ov,2)
                        match_info.second_ins_wkts = match_info.second_ins_wkts+1
                        match_info.save()
            else:
                if wicket_is_run == "True":
                    ba = cal_ball(match_info.first_ins_overs)+1
                    ov = cal_over(ba)
                    match_info.first_ins_runs = match_info.first_ins_runs+run
                    match_info.first_ins_overs = ov
                    match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
                    match_info.first_ins_wkts = match_info.first_ins_wkts+1
                    match_info.save()
                else:
                    if wicket_is_leg_bye == "True":
                        ba = cal_ball(match_info.first_ins_overs)+1
                        ov = cal_over(ba)
                        match_info.first_ins_runs = match_info.first_ins_runs+run
                        match_info.first_ins_overs = ov
                        match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
                        match_info.first_ins_wkts = match_info.first_ins_wkts+1
                        match_info.save()
                    else:
                        ba = cal_ball(match_info.first_ins_overs)
                        ov = cal_over(ba)
                        match_info.first_ins_runs = match_info.first_ins_runs+run
                        match_info.first_ins_overs = ov
                        match_info.first_ins_crr = round((match_info.first_ins_runs+run)/ov,2)
                        match_info.first_ins_wkts = match_info.first_ins_wkts+1
                        match_info.save()


            if run%2 == 0:
                if wicket_is_run == "True":
                    stricker.bat_runs = stricker.bat_runs+run
                    stricker.bat_balls= stricker.bat_balls+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                    stricker.save()
                else:
                    if wicket_is_leg_bye == "True":
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls+1 
                        stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                        stricker.save()
                    else:
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls
                        stricker.save()
            else:
                if wicket_is_run == "True":
                    stricker.bat_runs = stricker.bat_runs+run
                    stricker.bat_balls= stricker.bat_balls+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                    stricker.bat_is_striker = False
                    stricker.save()
                    non_stricker.bat_is_striker = True
                    non_stricker.save()
                else:
                    if wicket_is_leg_bye == "True":
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls+1 
                        stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                        stricker.bat_is_striker = False
                        stricker.save()
                        non_stricker.bat_is_striker = True
                        non_stricker.save()
                    else:
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls
                        stricker.bat_is_striker = False
                        stricker.save()
                        non_stricker.bat_is_striker = True
                        non_stricker.save()

            bowler__player = bowler[0]
            if wicket_is_run == "True":
                bba = cal_ball(bowler__player.bowl_over)+1
                bov = cal_over(bba)
                if bba == 0:
                    eco = -run
                else:
                    eco = (bowler__player.bowl_runs+run)/bov
                bowler__player.bowl_runs=bowler__player.bowl_runs+run
                bowler__player.bowl_over=bov
                bowler__player.bowl_economy=round(eco,2)
            else:
                if wicket_is_leg_bye == "True":
                    bba = cal_ball(bowler__player.bowl_over)+1
                    bov = cal_over(bba)
                    if bba == 0:
                        eco = -run
                    else:
                        eco = (bowler__player.bowl_runs+run)/bov
                    bowler__player.bowl_runs=bowler__player.bowl_runs
                    bowler__player.bowl_over=bov
                    bowler__player.bowl_economy=round(eco,2)
                else:
                    bba = cal_ball(bowler__player.bowl_over)
                    bov = cal_over(bba)
                    if bba == 0:
                        eco = -run
                    else:
                        eco = (bowler__player.bowl_runs+run)/bov
                    bowler__player.bowl_runs=bowler__player.bowl_runs
                    bowler__player.bowl_over=bov
                    bowler__player.bowl_economy=round(eco,2)
            if is_run_out == "False":
                bowler__player.bowl_wicket=bowler__player.bowl_wicket+1
            bowler__player.save()
            

            od = OverDetails.objects.filter(over_status = True,matchinfo = match_info_id,player = bowler__player.player.id).order_by('-created_at').first()
            if od.ball_count == 0:
                if wicket_is_run == "True":
                    od.over_runs = od.over_runs + run
                    od.ball_count = 1
                    od.over_ball_one = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye == "True":
                        od.over_runs = od.over_runs + run
                        od.ball_count = 1
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 1:
                if wicket_is_run == "True" :
                    od.over_runs = od.over_runs + run
                    od.ball_count = 2
                    od.over_ball_two = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye == "True":
                        od.over_runs = od.over_runs + run
                        od.ball_count = 2
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 2:
                if wicket_is_run == "True":
                    od.over_runs = od.over_runs + run
                    od.ball_count = 3
                    od.over_ball_three = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye == "True":
                        od.over_runs = od.over_runs + run
                        od.ball_count = 3
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 3:
                if wicket_is_run == "True":
                    od.over_runs = od.over_runs + run
                    od.ball_count = 4
                    od.over_ball_four = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye == "True":
                        od.over_runs = od.over_runs + run
                        od.ball_count = 4
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 4:
                if wicket_is_run == "True":
                    od.over_runs = od.over_runs + run
                    od.ball_count = 5
                    od.over_ball_five = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye:
                        od.over_runs = od.over_runs + run
                        od.ball_count = 5
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 5:
                if wicket_is_run == "True":
                    od.over_runs = od.over_runs + run
                    od.ball_count = 6
                    od.over_ball_six = run
                    od.over_wicket = od.over_wicket+1
                else:
                    od.over_run_bue = od.over_run_bye + run
                    if wicket_is_leg_bye == "True":
                        od.over_runs = od.over_runs + run
                        od.ball_count = 6
                        od.over_wicket = od.over_wicket+1
                    else:
                        od.over_runs = od.over_runs + run
                        od.over_wicket = od.over_wicket+1
                od.save()
            elif od.ball_count == 6:
                od.over_status = False
                od.over_wicket = od.over_wicket+1
                od.save()
            
            
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
                #recent bowler
                recent_bowler  = PlayerScore.objects.filter(matchinfo = match_info_id,bowl_status = "Recent").exclude(id = bowler__player.id)
                if recent_bowler.exists():
                    rec_bowl = recent_bowler.first()
                    rec_bowl.bowl_status = "Not Bowling"
                    rec_bowl.save()

            ## fall of wicket
            wicket_batter  = PlayerScore.objects.get(id=player_score_id)
            wicket_batter.bat_status = "Out"
            wicket_batter.save()

            ## fall wicket details
            if match_info.first_ins_complete:
                if is_run_out == "True":
                    FallWicket.objects.create(matchinfo=match_info,team = match_info.second_ins,run=match_info.second_ins_runs,wicket=match_info.second_ins_wkts,over=match_info.second_ins_overs,run_rate=match_info.second_ins_crr,batter=wicket_batter.player
                    )
                else:
                    FallWicket.objects.create(matchinfo=match_info,team = match_info.second_ins,run=match_info.second_ins_runs,wicket=match_info.second_ins_wkts,over=match_info.second_ins_overs,run_rate=match_info.second_ins_crr,batter=wicket_batter.player,bowler=bowler__player.player
                    )
            else:
                if is_run_out == "True":
                    FallWicket.objects.create(matchinfo=match_info,team = match_info.first_ins,run=match_info.first_ins_runs,wicket=match_info.first_ins_wkts,over=match_info.first_ins_overs,run_rate=match_info.first_ins_crr,batter=wicket_batter.player
                    )
                else:
                    FallWicket.objects.create(matchinfo=match_info,team = match_info.first_ins,run=match_info.first_ins_runs,wicket=match_info.first_ins_wkts,over=match_info.first_ins_overs,run_rate=match_info.first_ins_crr,batter=wicket_batter.player,bowler=bowler__player.player
                    )

            player = Players.objects.filter(id__in=batter.values('player'))
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))
            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
            data={
            "message":"success",
            "status":True,
            "players":PlayerImageSerializer(player,many=True).data,
            "score":BatScoreSerializer(score,many=True).data,

            "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
            "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

            "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
            "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
            "matchinfo":MatchinfoSerializer(match_info).data,
            "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player = bowler__player.player.id).order_by('created_at'),many=True).data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_update_noball(request):
    try:
        match_info_id = request.GET.get('match_info')
        player_score_id = request.GET.get('player_score_id')
        is_noball_out = request.GET.get('is_noball_out')
        noball_is_run = request.GET.get('noball_is_run')
        if noball_is_run == "True":
            run = int(request.GET.get('noball_hit_run'))
        else:
            run = int(request.GET.get('noball_extra_runs'))
            noball_is_leg_bye = request.GET.get('noball_is_leg_bye')


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
                if noball_is_run == "True":
                    ba = cal_ball(match_info.second_ins_overs)
                    ov = cal_over(ba)
                    match_info.second_ins_runs = match_info.second_ins_runs+run+1
                    match_info.second_ins_overs = ov
                    match_info.second_ins_extra_nb = match_info.second_ins_extra_nb+1
                    match_info.second_ins_extra_bye = match_info.second_ins_extra_bye+run
                    match_info.second_ins_crr = round((match_info.second_ins_runs+run+1)/ov,2)
                    if is_noball_out == "True":
                        match_info.second_ins_wkts = match_info.second_ins_wkts+1
                    match_info.save()
                else:
                    ba = cal_ball(match_info.second_ins_overs)
                    ov = cal_over(ba)
                    match_info.second_ins_runs = match_info.second_ins_runs+run+1
                    match_info.second_ins_overs = ov
                    match_info.second_ins_extra_nb = match_info.second_ins_extra_nb+1
                    match_info.second_ins_extra_bye = match_info.second_ins_extra_bye+run
                    match_info.second_ins_crr = round((match_info.second_ins_runs+run+1)/ov,2)
                    if is_noball_out == "True":
                        match_info.second_ins_wkts = match_info.second_ins_wkts+1
                    match_info.save()
                    
            else:
                if noball_is_run == "True":
                    ba = cal_ball(match_info.first_ins_overs)
                    ov = cal_over(ba)
                    match_info.first_ins_runs = match_info.first_ins_runs+run+1
                    match_info.first_ins_overs = ov
                    match_info.first_ins_extra_nb = match_info.first_ins_extra_nb+1
                    match_info.first_ins_extra_bye = match_info.first_ins_extra_bye+1
                    match_info.first_ins_crr = round((match_info.first_ins_runs+run+1)/ov,2)
                    if is_noball_out == "True":
                        match_info.first_ins_wkts = match_info.first_ins_wkts+1
                    match_info.save()
                else:
                    ba = cal_ball(match_info.first_ins_overs)
                    ov = cal_over(ba)
                    match_info.first_ins_runs = match_info.first_ins_runs+run+1
                    match_info.first_ins_overs = ov
                    match_info.first_ins_extra_nb = match_info.first_ins_extra_nb+1
                    match_info.first_ins_extra_bye = match_info.first_ins_extra_bye+run
                    match_info.first_ins_crr = round((match_info.first_ins_runs+run+1)/ov,2)
                    if is_noball_out == "True":
                        match_info.first_ins_wkts = match_info.first_ins_wkts+1
                    match_info.save()


            if run%2 == 0:
                if noball_is_run == "True":
                    stricker.bat_runs = stricker.bat_runs+run
                    stricker.bat_balls= stricker.bat_balls+1
                    if run == 4: 
                        stricker.bat_fours= stricker.bat_fours+1 
                    if run == 6:
                        stricker.bat_sixes= stricker.bat_sixes+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                    stricker.save()
                else:
                    if noball_is_leg_bye == "True":
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls+1 
                        stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                        stricker.save()
                    else:
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls
                        stricker.save()
            else:
                if noball_is_run == "True":
                    stricker.bat_runs = stricker.bat_runs+run
                    stricker.bat_balls= stricker.bat_balls+1 
                    stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                    stricker.bat_is_striker = False
                    stricker.save()
                    non_stricker.bat_is_striker = True
                    non_stricker.save()
                else:
                    if noball_is_leg_bye == "True":
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls+1 
                        stricker.bat_strike_rate = round(((stricker.bat_runs+run)/(stricker.bat_balls+1))*100,2)
                        stricker.bat_is_striker = False
                        stricker.save()
                        non_stricker.bat_is_striker = True
                        non_stricker.save()
                    else:
                        stricker.bat_runs = stricker.bat_runs
                        stricker.bat_balls= stricker.bat_balls
                        stricker.bat_is_striker = False
                        stricker.save()
                        non_stricker.bat_is_striker = True
                        non_stricker.save()

            bowler__player = bowler[0]
            if noball_is_run == "True":
                bba = cal_ball(bowler__player.bowl_over)
                bov = cal_over(bba)
                if bba == 0:
                    eco = -run
                else:
                    eco = (bowler__player.bowl_runs+run+1)/bov
                bowler__player.bowl_runs=bowler__player.bowl_runs+run+1
                bowler__player.bowl_over=bov
                bowler__player.bowl_economy=round(eco,2)
            else:
                bba = cal_ball(bowler__player.bowl_over)
                bov = cal_over(bba)
                if bba == 0:
                    eco = -run
                else:
                    eco = (bowler__player.bowl_runs+1)/bov
                bowler__player.bowl_runs=bowler__player.bowl_runs+1
                bowler__player.bowl_over=bov
                bowler__player.bowl_economy=round(eco,2)
            bowler__player.save()
            

            od = OverDetails.objects.filter(over_status = True,matchinfo = match_info_id,player = bowler__player.player.id).order_by('-created_at').first()
            if noball_is_run == "True":
                od.over_runs = od.over_runs + run+1
                od.over_run_nb = od.over_run_nb+1
            else:
                od.over_runs = od.over_runs + run
                od.over_run_bye = od.over_run_bye + run
            od.save()
            
            
            ## fall of wicket
            if is_noball_out == "True":
                wicket_batter  = PlayerScore.objects.get(id=player_score_id)
                wicket_batter.bat_status = "Out"
                wicket_batter.save()

                ## fall wicket details
                if match_info.first_ins_complete:
                        FallWicket.objects.create(matchinfo=match_info,team = match_info.second_ins,run=match_info.second_ins_runs,wicket=match_info.second_ins_wkts,over=match_info.second_ins_overs,run_rate=match_info.second_ins_crr,batter=wicket_batter.player)
                else:
                    FallWicket.objects.create(matchinfo=match_info,team = match_info.first_ins,run=match_info.first_ins_runs,wicket=match_info.first_ins_wkts,over=match_info.first_ins_overs,run_rate=match_info.first_ins_crr,batter=wicket_batter.player)
                    

            player = Players.objects.filter(id__in=batter.values('player'))
            player_bowl = Players.objects.filter(id__in=bowler.values('player'))
            score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player.values('id'))
            bowl_score = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = player_bowl.values('id'))
            playingsquardA = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in= Players.objects.filter(team=match_info.first_ins.id).values('id'))
            playingsquardB = PlayingSquard.objects.filter(is_play = True,schedule = match_info.schedule.id,player__in=Players.objects.filter(team=match_info.second_ins.id).values('id'))
            squardA = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardA.values('player')).order_by('-updated_at')
            squardB = PlayerScore.objects.filter(matchinfo = match_info_id,player__in = playingsquardB.values('player')).order_by('-updated_at')
            data={
            "message":"success",
            "status":True,
            "players":PlayerImageSerializer(player,many=True).data,
            "score":BatScoreSerializer(score,many=True).data,

            "player_bowl":PlayerImageSerializer(player_bowl,many=True).data,
            "bowl_score":BowlScoreSerializer(bowl_score,many=True).data,

            "squardA":PlayerSquardScoreSerializer(squardA,many=True).data,
            "squardB":PlayerSquardScoreSerializer(squardB,many=True).data,
            "matchinfo":MatchinfoSerializer(match_info).data,
            "over_details":OverDetailsSerializer(OverDetails.objects.filter(matchinfo = match_info_id,player = bowler__player.player.id).order_by('created_at'),many=True).data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_complete_first_inn(request):
    try:
        match_info_id = request.GET.get('match_info')        
        match_info = MatchInfo.objects.get(id = match_info_id)
        
        with transaction.atomic():
            sc = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(bat_status ="Batting")|Q(bat_status ="Out"))
            for i in sc:
                pl = Players.objects.get(id=i.player.id)
                pl.bat_runs = pl.bat_runs +  i.bat_runs
                pl.bat_balls = pl.bat_balls + i.bat_balls
                pl.bat_fours = pl.bat_fours + i.bat_fours
                pl.bat_sixes = pl.bat_sixes + i.bat_sixes
                if i.bat_runs >= 50:
                    pl.bat_thirty = pl.bat_thirty  + 1
                elif i.bat_runs >= 30: 
                    pl.bat_fifty = pl.bat_fifty  + 1
                if pl.bat_high_score < i.bat_runs:
                    pl.bat_high_score = i.bat_runs
                av  = (pl.bat_runs + i.bat_runs) / (pl.bat_ins+1)
                pl.bat_average = av
                pl.bat_strike_rate = (pl.bat_strike_rate + i.bat_strike_rate) / (pl.bat_ins+1)
                pl.bat_ins = pl.bat_ins+1
                pl.save()

            scb = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(bowl_status ="Bowling")|Q(bowl_status ="Recent")|Q(bowl_status ="Bowled"))
            for i in scb:
                pl = Players.objects.get(id=i.player.id)
                pl.bowl_wicket = pl.bowl_wicket +  i.bowl_wicket
                pl.bowl_runs = pl.bowl_runs +  i.bowl_runs
                ovtball = cal_ball(i.bowl_over)
                pl.bowl_balls = pl.bowl_balls + ovtball

                if i.bowl_wicket >= 5:
                    pl.bowl_five_wkt = pl.bowl_five_wkt  + 1
                elif i.bowl_wicket >= 3: 
                    pl.bowl_three_wkt = pl.bowl_three_wkt  + 1

                if pl.bowl_best_bowling < i.bowl_wicket:
                    pl.bowl_best_bowling = i.bowl_wicket

                av  = (pl.bowl_wicket + i.bowl_wicket) / (pl.bowl_ins+1)
                pl.bowl_average = av
                pl.bowl_economy = (pl.bowl_economy + i.bowl_economy) / (pl.bowl_ins+1)
                pl.bowl_ins = pl.bowl_ins+1
                pl.save()

            match_info.first_ins_complete = True
            match_info.save()                
            data={
            "message":"success",
            "status":True
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


@api_view(['GET'])
@permission_classes([IsAuthenticated],)
def ajax_complete_second_inn(request):
    try:
        match_info_id = request.GET.get('match_info')        
        match_info = MatchInfo.objects.get(id = match_info_id)
        
        with transaction.atomic():
            sc = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(bat_status ="Batting")|Q(bat_status ="Out"))
            for i in sc:
                pl = Players.objects.get(id=i.player.id)
                pl.bat_runs = pl.bat_runs +  i.bat_runs
                pl.bat_balls = pl.bat_balls + i.bat_balls
                pl.bat_fours = pl.bat_fours + i.bat_fours
                pl.bat_sixes = pl.bat_sixes + i.bat_sixes
                if i.bat_runs >= 50:
                    pl.bat_thirty = pl.bat_thirty  + 1
                elif i.bat_runs >= 30: 
                    pl.bat_fifty = pl.bat_fifty  + 1
                if pl.bat_high_score < i.bat_runs:
                    pl.bat_high_score = i.bat_runs
                av  = (pl.bat_runs + i.bat_runs) / (pl.bat_ins+1)
                pl.bat_average = av
                pl.bat_strike_rate = (pl.bat_strike_rate + i.bat_strike_rate) / (pl.bat_ins+1)
                pl.bat_ins= pl.bat_ins +1
                pl.save()

            scb = PlayerScore.objects.filter(Q(matchinfo = match_info_id),Q(bowl_status ="Bowling")|Q(bowl_status ="Recent")|Q(bowl_status ="Bowled"))
            for i in scb:
                pl = Players.objects.get(id=i.player.id)
                pl.bowl_wicket = pl.bowl_wicket +  i.bowl_wicket
                pl.bowl_runs = pl.bowl_runs +  i.bowl_runs
                ovtball = cal_ball(i.bowl_over)
                pl.bowl_balls = pl.bowl_balls + ovtball

                if i.bowl_wicket >= 5:
                    pl.bowl_five_wkt = pl.bowl_five_wkt  + 1
                elif i.bowl_wicket >= 3: 
                    pl.bowl_three_wkt = pl.bowl_three_wkt  + 1

                if pl.bowl_best_bowling < i.bowl_wicket:
                    pl.bowl_best_bowling = i.bowl_wicket

                av  = (pl.bowl_wicket + i.bowl_wicket) / (pl.bowl_ins+1)
                pl.bowl_average = av
                pl.bowl_economy = (pl.bowl_economy + i.bowl_economy) / (pl.bowl_ins+1)
                pl.bowl_ins = pl.bowl_ins +1
                pl.save()

            match_info.seond_ins_complete = True
            if match_info.first_ins_runs > match_info.second_ins_runs:
                match_info.who_win = match_info.first_ins
                mat1= PointTable.objects.get(team = match_info.first_ins.id)
                mat1.matches = mat1.matches + 1
                mat1.win= mat1.win +1 
                mat1.point= mat1.point + 2
                rr = (match_info.first_ins_runs/match_info.first_ins_overs)-(match_info.second_ins_runs/match_info.second_ins_overs)
                mat1.run_rate= mat1.run_rate + round(rr,2)
                mat1.save()

                mat2 = PointTable.objects.get(team = match_info.second_ins.id)
                mat2.matches =  mat2.matches + 1
                mat2.lose = mat2.lose + 1 
                rr2 = (match_info.second_ins_runs/match_info.second_ins_overs)-(match_info.first_ins_runs/match_info.first_ins_overs)
                mat2.run_rate= mat2.run_rate + round(rr2,2)
                mat2.save()

            else:
                match_info.who_win =  match_info.second_ins
                mat2 = PointTable.objects.get(team = match_info.second_ins.id)
                mat2.matches =  mat2.matches + 1
                mat2.win = mat2.win + 1 
                mat2.point = mat2.point + 2
                rr = (match_info.second_ins_runs/match_info.second_ins_overs)-(match_info.first_ins_runs/match_info.first_ins_overs)
                mat2.run_rate= mat2.run_rate + round(rr,2)
                mat2.save()
                
                mat1= PointTable.objects.get(team = match_info.first_ins.id)
                mat1.matches = mat1.matches + 1
                mat1.lose= mat1.lose +1 

                rr1 = (match_info.first_ins_runs/match_info.first_ins_overs)-(match_info.second_ins_runs/match_info.second_ins_overs)
                mat1.run_rate= mat1.run_rate + round(rr1,2)
                mat1.save()

            match_info.save()
            sch = Schedule.objects.get(id = match_info.schedule.id)
            sch.status= "Complete"
            sch.save()
              

            
            data={
            "message":"success",
            "status":True
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


def complete_task_schedules(request):
    sc  = Schedule.objects.filter(schedule_date__date = datetime.now().date()).first()
    if sc.status == "Incomplete":
        sc.status ="Today"
        sc.save()
        return HttpResponseRedirect(reverse('schedule_details',kwargs={"id":sc.id}))
    else:
        return HttpResponseRedirect(reverse('dashboard'))


    