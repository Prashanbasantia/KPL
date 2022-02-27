from numpy import place
from rest_framework import serializers
from Admin_App.models import *

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['name']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['id','name']

class PlayerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['id','name','image']

class MatchinfoSerializer(serializers.ModelSerializer):
    first_ins=TeamSerializer()
    second_ins=TeamSerializer()
    class Meta:
        model = MatchInfo
        fields = ['first_ins_complete','first_ins_crr','toss_own','toss_own_options','first_ins','first_ins_runs','first_ins_wkts','first_ins_overs','second_ins','second_ins_runs','second_ins_wkts','second_ins_overs','second_ins_crr','first_ins_extra_runs','second_ins_extra_runs','second_ins_extra_wd','second_ins_extra_nb','second_ins_extra_bye','first_ins_extra_wd','first_ins_extra_nb','first_ins_extra_bye','first_ins_complete','second_ins_complete']

class PlayerSquardScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['player','bat_runs','bat_strike_rate','bat_is_striker','bat_fours','bat_sixes','bat_balls','bat_status','bowl_status' ,'bowl_over','bowl_wicket','bowl_runs','bowl_economy']


class BowlScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['player','bowl_runs','bowl_over','bowl_economy','bowl_wicket','bowl_status']

class BatScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['player','bat_is_striker','bat_runs','bat_balls','bat_strike_rate','bat_fours','bat_sixes','bat_status']


class WicketPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['id','bat_is_striker','player']



class OverDetailsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = OverDetails
        fields = ['over_runs','over_wicket','player','over_wicket','over_ball_one','over_ball_two','over_ball_three','over_ball_four','over_ball_five','over_ball_six','over_run_wd','over_run_nb','over_run_bye','ball_count']