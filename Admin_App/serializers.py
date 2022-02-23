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
        fields = ['first_ins_complete','first_ins_crr','toss_own','toss_own_options','first_ins','first_ins_runs','first_ins_wkts','first_ins_overs','second_ins','second_ins_runs','second_ins_wkts','second_ins_overs','second_ins_crr','first_ins_extra_runs','second_ins_extra_runs','second_ins_extra_wd','second_ins_extra_nb','second_ins_extra_bye','first_ins_extra_wd','first_ins_extra_nb','first_ins_extra_bye']

class PlayerSquardScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['player','bat_runs','bat_strike_rate','bat_balls','bowl_over','bowl_wicket','bowl_runs','bowl_economy']


class BowlScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerScore
        fields = ['bowl_runs','bowl_over','bowl_economy','bowl_wicket']

class BatScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerScore
        fields = ['bat_is_striker','bat_runs','bat_balls','bat_strike_rate','bat_fours','bat_sixes']


class WicketPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['id','bat_is_striker','player']



class OverDetailsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = OverDetails
        fields = ['over_runs','over_wicket','player','over_wicket','over_ball_one','over_ball_two','over_ball_three','over_ball_four','over_ball_five','over_run_wd','over_run_nb','over_run_bye','ball_count']