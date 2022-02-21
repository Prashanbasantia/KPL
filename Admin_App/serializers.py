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
        fields = ['first_ins_complete','first_ins_crr','toss_own','toss_own_options','first_ins','first_ins_runs','first_ins_wkts','first_ins_overs','second_ins','second_ins_runs','second_ins_wkts','second_ins_overs','second_ins_crr']

class PlayerSquardScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = PlayerScore
        fields = ['player','bat_runs','bat_balls','bowl_over','bowl_wicket']


class BowlScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerScore
        fields = ['bowl_runs','bowl_over','bowl_economy','bowl_wicket']

class BatScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerScore
        fields = ['bat_is_striker','bat_runs','bat_balls','bat_strike_rate','bat_fours','bat_sixes']