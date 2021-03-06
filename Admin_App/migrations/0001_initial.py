# Generated by Django 3.2.4 on 2022-02-23 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_toss', models.BooleanField(default=False)),
                ('toss_own', models.CharField(default='Team A', max_length=120)),
                ('toss_own_options', models.CharField(default='Elected To Bat First', max_length=120)),
                ('first_ins_runs', models.IntegerField(default=0)),
                ('first_ins_extra_runs', models.IntegerField(default=0)),
                ('first_ins_extra_wd', models.IntegerField(default=0)),
                ('first_ins_extra_nb', models.IntegerField(default=0)),
                ('first_ins_extra_bye', models.IntegerField(default=0)),
                ('first_ins_wkts', models.IntegerField(default=0)),
                ('first_ins_overs', models.FloatField(default=0.0)),
                ('first_ins_crr', models.FloatField(default=0.0)),
                ('first_ins_complete', models.BooleanField(default=False)),
                ('second_ins_runs', models.IntegerField(default=0)),
                ('second_ins_extra_runs', models.IntegerField(default=0)),
                ('second_ins_extra_wd', models.IntegerField(default=0)),
                ('second_ins_extra_nb', models.IntegerField(default=0)),
                ('second_ins_extra_bye', models.IntegerField(default=0)),
                ('second_ins_wkts', models.IntegerField(default=0)),
                ('second_ins_overs', models.FloatField(default=0.0)),
                ('second_ins_crr', models.FloatField(default=0.0)),
                ('second_ins_complete', models.BooleanField(default=False)),
                ('umpire_one', models.CharField(default='Mr Swain', max_length=100)),
                ('umpire_two', models.CharField(default='Mr Rout', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('image', models.ImageField(default='player_image/default_player.png', upload_to='player_image/')),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=225)),
                ('role', models.CharField(choices=[('Batsman', 'Bsn'), ('Bowler', 'Blr'), ('Allrounder', 'Ar'), ('Batting Allrounder', 'Bta'), ('Bowling Allrounder', 'Bwa')], default='Batsman', max_length=100)),
                ('batting_style', models.CharField(choices=[('Right Handed Bat', 'RHB'), ('Left Handed Bat', 'LHB')], default='Right Handed Bat', max_length=100)),
                ('bowling_style', models.CharField(choices=[('Right-arm Fast-medium', 'RFM'), ('Left-arm Fast-medium', 'LFM'), ('Right-arm Medium', 'RM'), ('Left-arm Medium', 'LM'), ('Right-arm Offbreak', 'RAO'), ('Right-arm Legbreak', 'RAl'), ('Left-arm Legbreak', 'LAL'), ('Left-arm Offbreak', 'LAO')], default='Right-arm Fast-medium', max_length=100)),
                ('match', models.IntegerField(default=0)),
                ('ins', models.IntegerField(default=0)),
                ('bat_runs', models.IntegerField(default=0)),
                ('bat_balls', models.IntegerField(default=0)),
                ('bat_strike_rate', models.FloatField(default=0.0)),
                ('bat_average', models.FloatField(default=0.0)),
                ('bat_high_score', models.IntegerField(default=0)),
                ('bat_fours', models.IntegerField(default=0)),
                ('bat_sixes', models.IntegerField(default=0)),
                ('bat_thirty', models.IntegerField(default=0)),
                ('bat_fifty', models.IntegerField(default=0)),
                ('bowl_wicket', models.IntegerField(default=0)),
                ('bowl_runs', models.IntegerField(default=0)),
                ('bowl_balls', models.IntegerField(default=0)),
                ('bowl_economy', models.FloatField(default=0.0)),
                ('bowl_average', models.FloatField(default=0.0)),
                ('bowl_best_bowling', models.IntegerField(default=0)),
                ('bowl_three_wkt', models.IntegerField(default=0)),
                ('bowl_five_wkt', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('short_name', models.CharField(max_length=225)),
                ('logo', models.ImageField(default='team_logo/default_team.png', upload_to='team_logo/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.seasons')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_type', models.CharField(choices=[('League', 'L'), ('Qualifier', 'Q'), ('Final', 'F')], default='League', max_length=100)),
                ('schedule_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Incomplete', 'In'), ('Live', 'Li'), ('Complete', 'Co'), ('Today', 'Td')], default='Incomplete', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamone', to='Admin_App.teams')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamtwo', to='Admin_App.teams')),
            ],
        ),
        migrations.CreateModel(
            name='PointTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matches', models.IntegerField(default=0)),
                ('win', models.IntegerField(default=0)),
                ('lose', models.IntegerField(default=0)),
                ('point', models.IntegerField(default=0)),
                ('run_rate', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.teams')),
            ],
        ),
        migrations.CreateModel(
            name='PlayingSquard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_play', models.BooleanField(default=False)),
                ('is_captain', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.players')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bat_status', models.CharField(choices=[('Not Batting', 'Nbt'), ('Batting', 'Bt'), ('Out', 'ot'), ('Not Out', 'not')], default='Not Batting', max_length=100)),
                ('bat_is_striker', models.BooleanField(default=False)),
                ('bat_runs', models.IntegerField(default=0)),
                ('bat_balls', models.IntegerField(default=0)),
                ('bat_strike_rate', models.FloatField(default=0.0)),
                ('bat_fours', models.IntegerField(default=0)),
                ('bat_sixes', models.IntegerField(default=0)),
                ('bowl_status', models.CharField(choices=[('Not Bowling', 'Nbw'), ('Bowling', 'Bw'), ('Recent', 'Bw')], default='Not Bowling', max_length=100)),
                ('bowl_runs', models.IntegerField(default=0)),
                ('bowl_over', models.FloatField(default=0.0)),
                ('bowl_economy', models.FloatField(default=0.0)),
                ('bowl_wicket', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('matchinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.matchinfo')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.players')),
            ],
        ),
        migrations.AddField(
            model_name='players',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Admin_App.teams'),
        ),
        migrations.CreateModel(
            name='OverDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('over_status', models.BooleanField(default=False)),
                ('over_runs', models.IntegerField(default=0)),
                ('ball_count', models.IntegerField(default=0)),
                ('over_wicket', models.IntegerField(default=0)),
                ('over_ball_one', models.IntegerField(default=0)),
                ('over_ball_two', models.IntegerField(default=0)),
                ('over_ball_three', models.IntegerField(default=0)),
                ('over_ball_four', models.IntegerField(default=0)),
                ('over_ball_five', models.IntegerField(default=0)),
                ('over_ball_six', models.IntegerField(default=0)),
                ('over_run_wd', models.IntegerField(default=0)),
                ('over_run_nb', models.IntegerField(default=0)),
                ('over_run_bye', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('matchinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.matchinfo')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.players')),
            ],
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='first_ins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_ins', to='Admin_App.teams'),
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.schedule'),
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='second_ins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_ins', to='Admin_App.teams'),
        ),
        migrations.AddField(
            model_name='matchinfo',
            name='who_win',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='win_team', to='Admin_App.teams'),
        ),
        migrations.CreateModel(
            name='FallWicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.IntegerField(default=0)),
                ('wicket', models.IntegerField(default=0)),
                ('over', models.IntegerField(default=0)),
                ('run_rate', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('batter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batter', to='Admin_App.players')),
                ('bowler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bowler', to='Admin_App.players')),
                ('matchinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.matchinfo')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.teams')),
            ],
        ),
    ]
