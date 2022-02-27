from re import S
from django.db import models

# Create your models here.
class Seasons(models.Model):
    id = models.AutoField(primary_key=True)
    year=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Teams(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=225)
    short_name=models.CharField(max_length=225)
    season = models.ForeignKey(Seasons,on_delete=models.CASCADE)
    logo = models.ImageField(upload_to ="team_logo/",default='team_logo/default_team.png')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Players(models.Model):
    role_choice=[("Batsman","Bsn"),("Bowler","Blr"),("Allrounder","Ar"),("Batting Allrounder","Bta"),("Bowling Allrounder","Bwa")]
    batting_style_choice=[("Right Handed Bat","RHB"),("Left Handed Bat","LHB")]
    bowling_style_choice=[("Right-arm Fast-medium","RFM"),("Left-arm Fast-medium","LFM"),("Right-arm Medium","RM"),("Left-arm Medium","LM"),("Right-arm Offbreak","RAO"),("Right-arm Legbreak","RAl"),("Left-arm Legbreak","LAL"),("Left-arm Offbreak","LAO")]
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Teams,on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=225)
    image = models.ImageField(upload_to ="player_image/",default='player_image/default_player.png')
    age=models.IntegerField()
    address=models.CharField(max_length=225)
    role=models.CharField(default="Batsman",choices=role_choice,max_length=100)
    batting_style=models.CharField(default="Right Handed Bat",choices=batting_style_choice,max_length=100)
    bowling_style=models.CharField(default="Right-arm Fast-medium",choices=bowling_style_choice,max_length=100)
    #stats
    match=models.IntegerField(default=0)
    bat_ins=models.IntegerField(default=0)
    bowl_ins=models.IntegerField(default=0)

    bat_runs=models.IntegerField(default=0)
    bat_balls=models.IntegerField(default=0)
    bat_strike_rate=models.FloatField(default=0.0)
    bat_average=models.FloatField(default=0.0)
    bat_high_score=models.IntegerField(default=0)
    bat_fours=models.IntegerField(default=0)
    bat_sixes=models.IntegerField(default=0)
    bat_thirty=models.IntegerField(default=0)
    bat_fifty=models.IntegerField(default=0)

    bowl_wicket=models.IntegerField(default=0)
    bowl_runs=models.IntegerField(default=0)
    bowl_balls=models.IntegerField(default=0)
    bowl_economy=models.FloatField(default=0.0)
    bowl_average=models.FloatField(default=0.0)
    bowl_best_bowling=models.IntegerField(default=0)
    bowl_three_wkt=models.IntegerField(default=0)
    bowl_five_wkt=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class Schedule(models.Model):
    match_choice=[("League","L"),("Qualifier","Q"),("Final","F")]
    team_one = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='teamone')
    team_two = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='teamtwo')
    match_type=models.CharField(default="League",choices=match_choice,max_length=100)
    schedule_date = models.DateTimeField()
    status_choice=[("Incomplete","In"),("Live","Li"),("Complete","Co"),("Today","Td")]
    status=models.CharField(default="Incomplete",choices=status_choice,max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class MatchInfo(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)       
    is_toss=models.BooleanField(default=False)#True means Team one Fasle means Team Two
    toss_own=models.CharField(default="Team A",max_length=120)#True means Team one Fasle means Team Two
    toss_own_options=models.CharField(default="Elected To Bat First",max_length=120)#True means batting Fasle means Bowling
    
    first_ins = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='first_ins')
    first_ins_runs = models.IntegerField(default=0)
    first_ins_extra_runs = models.IntegerField(default=0)
    first_ins_extra_wd = models.IntegerField(default=0)
    first_ins_extra_nb = models.IntegerField(default=0)
    first_ins_extra_bye = models.IntegerField(default=0)
    first_ins_wkts = models.IntegerField(default=0)
    first_ins_overs = models.FloatField(default=0.0)
    first_ins_crr = models.FloatField(default=0.0)
    first_ins_complete = models.BooleanField(default=False)

    second_ins = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='second_ins')
    second_ins_runs = models.IntegerField(default=0)
    second_ins_extra_runs = models.IntegerField(default=0)
    second_ins_extra_wd = models.IntegerField(default=0)
    second_ins_extra_nb = models.IntegerField(default=0)
    second_ins_extra_bye = models.IntegerField(default=0)
    second_ins_wkts = models.IntegerField(default=0)
    second_ins_overs = models.FloatField(default=0.0)
    second_ins_crr = models.FloatField(default=0.0)
    second_ins_complete = models.BooleanField(default=False)

    who_win=models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='win_team',null=True)#True means Team one Fasle means Team Two
    umpire_one=models.CharField(default="Mr Swain",max_length=100)
    umpire_two=models.CharField(default="Mr Rout",max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class PlayerScore(models.Model):
    id = models.AutoField(primary_key=True)
    matchinfo = models.ForeignKey(MatchInfo,on_delete=models.CASCADE)
    player = models.ForeignKey(Players,on_delete=models.CASCADE)
    bowling_choice=[("Not Bowling","Nbw"),("Bowling","Bw"),("Recent","Bw"),("Bowled","Bwl")]
    batting_choice=[("Not Batting","Nbt"),("Batting","Bt"),("Out","ot"),("Continue Bat","cbl")]

    is_bat_inn_one = models.BooleanField(default=False)
    is_bat_inn_two = models.BooleanField(default=False)
    is_bowl_inn_one = models.BooleanField(default=False)
    is_bowl_inn_two = models.BooleanField(default=False)

    bat_status=models.CharField(default="Not Batting",choices=batting_choice,max_length=100)
    bat_is_striker = models.BooleanField(default=False)
    bat_runs=models.IntegerField(default=0)
    bat_balls=models.IntegerField(default=0)
    bat_strike_rate=models.FloatField(default=0.0)
    bat_fours=models.IntegerField(default=0)
    bat_sixes=models.IntegerField(default=0)

    bowl_status=models.CharField(default="Not Bowling",choices=bowling_choice,max_length=100)
    bowl_runs=models.IntegerField(default=0)
    bowl_over=models.FloatField(default=0.0)
    bowl_economy=models.FloatField(default=0.0)
    bowl_wicket=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class OverDetails(models.Model):
    id = models.AutoField(primary_key=True)
    matchinfo = models.ForeignKey(MatchInfo,on_delete=models.CASCADE)
    player = models.ForeignKey(Players,on_delete=models.CASCADE)
    over_status=models.BooleanField(default=False)
    
    over_runs=models.IntegerField(default=0)
    ball_count=models.IntegerField(default=0)
    over_wicket=models.IntegerField(default=0)

    over_ball_one=models.IntegerField(default=0)
    over_ball_two=models.IntegerField(default=0)
    over_ball_three=models.IntegerField(default=0)
    over_ball_four=models.IntegerField(default=0)
    over_ball_five=models.IntegerField(default=0)
    over_ball_six=models.IntegerField(default=0)

    over_run_wd = models.IntegerField(default=0)
    over_run_nb = models.IntegerField(default=0)
    over_run_bye = models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class PlayingSquard(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)       
    player = models.ForeignKey(Players,on_delete=models.CASCADE)
    is_play=models.BooleanField(default=False)
    is_captain=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class PointTable(models.Model):
    team = models.ForeignKey(Teams,on_delete=models.CASCADE)
    matches=models.IntegerField(default=0)
    win=models.IntegerField(default=0)
    lose=models.IntegerField(default=0)
    point=models.IntegerField(default=0)
    run_rate=models.FloatField(default=0.0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class FallWicket(models.Model):
    matchinfo = models.ForeignKey(MatchInfo,on_delete=models.CASCADE)       
    team = models.ForeignKey(Teams,on_delete=models.CASCADE) 
    run=models.IntegerField(default=0)
    wicket=models.IntegerField(default=0)
    over=models.IntegerField(default=0)
    run_rate=models.FloatField(default=0.0)
    batter=models.ForeignKey(Players,on_delete=models.CASCADE,related_name='batter')
    bowler=models.ForeignKey(Players,on_delete=models.CASCADE,related_name='bowler',null=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)



