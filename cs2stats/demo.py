#https://stackoverflow.com/a/24456404
import datetime
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs2stats.settings")
django.setup()
from django.utils import timezone
from awpy import Demo
from stats.models import Player, Match, Stat, Team, Series, Round, Kills
#https://docs.djangoproject.com/en/5.0/ref/exceptions/
from django.core.exceptions import ObjectDoesNotExist
from awpy.stats import adr
from awpy.stats import kast
from awpy.stats import rating

def parseMatchFromDemo(dem, ctTeam, tTeam, series):

    if not series:
        series = Series(winningTeam="Undecided")
        series.save()

    #match
    match = Match()
    match.date=timezone.now()

    match.team_a=ctTeam
    match.team_b=tTeam
    match.map = dem.header['map_name'] 
    match.series_id = series
    match.save()


    #round
    for index, round in dem.rounds.iterrows():
        print(round['round'])
        print(dem.events['round_announce_last_round_half']['round'])

        # use the las round of the half to work out when the teams swap sides (and it even works for overtime)
        if (round['round']-1) in dem.events['round_announce_last_round_half']['round'].tolist():
            tmpCtTeam = ctTeam
            ctTeam = tTeam
            tTeam = tmpCtTeam


        #for some reason the winner is returned as a number (3=CT, 2=T)
        if (round['winner'] == "CT") or (round['winner'] == 3):
            winner = ctTeam
        else:
            winner = tTeam

        r=Round(match_id=match, round_num=round['round'], isWarmup=False, winningSide=round['winner'], winningTeam=winner, roundEndReason=round['reason'])
        r.save()

    #kills
    for index, kill in dem.kills.iterrows():
        # if it doesn't exist, print a message and skip to the next kill.
        try:
            round = Round.objects.filter(match_id=match).get(round_num=kill['round'])
        except ObjectDoesNotExist:
            print(f"round_num {kill['round']} does not exist for match {match}")
            continue
        
        #Not all kills will have assisters or even attackers as players can be killed by bomb or falling
        try:
            attacker = Player.objects.get(steam_id=kill['attacker_steamid'])
        except Player.DoesNotExist:
            print(f"Attacker with steam_id {kill['attacker_steamid']} does not exist")
            attacker = None
        try:
            assister = Player.objects.get(steam_id=kill['assister_steamid'])
        except Player.DoesNotExist:
            print(f"Assister with steam_id {kill['assister_steamid']} does not exist")
            assister = None
        try:
            victim = Player.objects.get(steam_id=kill['victim_steamid'])
        except Player.DoesNotExist:
            print(f"Victim with steam_id {kill['victim_steamid']} does not exist")
            victim = None

        
        if round:
            k = Kills(
                round_ID=round, 
                attackerSide=kill['attacker_team_name'], 
                victimSide=kill['victim_team_name'], 
                isHeadshot=kill['headshot'], 
                distance=0.0, 
                isTrade=False, 
                weapon=kill['weapon'], 
                weaponClass="weapons",
                tick=kill['tick'],
                round_time=kill['clock']
            )
            
            if attacker:
                k.attacker_ID = attacker
            if assister:
                k.assister_ID = assister
            if victim:
                k.victim_ID = victim
            
            k.save()
            
        else:
            print(f"Skipping kill due to missing round, attacker, or victim data: {kill}")

    #stats
    adr_stats = adr(dem)
    kast_stats = kast(dem)
    rating_stats = rating(dem)


    player_steam_ids = set(dem.kills['attacker_steamid']).union(set(dem.kills['victim_steamid']))
    for steam_id in player_steam_ids:
        
        try:
            player_instance = Player.objects.get(steam_id=steam_id)
        except Player.DoesNotExist:
            print(f"Player with steam_id {steam_id} does not exist")
            continue

        
        total_kills = len(dem.kills[dem.kills['attacker_steamid'] == steam_id])
        total_deaths = len(dem.kills[dem.kills['victim_steamid'] == steam_id])
        total_damage = dem.damages[dem.damages['attacker_steamid'] == steam_id]['dmg_health_real'].sum()
        rounds_played = len(dem.rounds)

        if rounds_played > 0:
            kills_per_round = total_kills / rounds_played
            deaths_per_round = total_deaths / rounds_played
            kd_ratio = total_kills / (total_deaths if total_deaths > 0 else 1)
            damage_per_round = total_damage / rounds_played
            headshot_percentage = (dem.kills[dem.kills['attacker_steamid'] == steam_id]['headshot'].mean()) * 100

            adr_df=adr_stats[(adr_stats['steamid']==steam_id) & (adr_stats['team_name']=='all')]
            kast_df=kast_stats[(kast_stats['steamid']==steam_id) & (kast_stats['team_name']=='all')]
            rating_df=rating_stats[(rating_stats['steamid']==steam_id) & (rating_stats['team_name']=='all')]

            
            adr_value = adr_df['adr']
            kast_value = kast_df['kast']
            rating_value = rating_df['rating']
            impact_value = rating_df['impact']
            
            stat, created = Stat.objects.update_or_create(
                player=player_instance,
                match=match,
                defaults={
                    'rating': rating_value,
                    'kills_per_round': kills_per_round,
                    'deaths_per_round': deaths_per_round,
                    'kd_ratio': kd_ratio,
                    'headshot_percentage': headshot_percentage,
                    'total_kills': total_kills,
                    'total_deaths': total_deaths,
                    'damage_per_round': damage_per_round,
                    'rounds_played': rounds_played,
                    'maps_played': 1,  
                    'win_percentage': 0,
                    'entry_kills': 0,
                    'adr': adr_value,
                    'kast': kast_value,
                    'impact': impact_value
                }
            )

            print(f"Updated stats for player {player_instance.nick_name}")


#dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem", ticks=True)
dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m2-anubis.dem", ticks=True)



#series 1
#series = Series.objects.get(id=1)
#make a new series
series = Series(winningTeam="Undecided")
series.save()

#ct_team = dem.events['begin_new_match'][['ct_team_clan_name']]
#t_team = dem.events['begin_new_match'][['t_team_clan_name']]

team_a = Team.objects.get(id=1) #navi
team_b = Team.objects.get(id=2) #vp

parseMatchFromDemo(dem=dem, ctTeam=team_a, tTeam=team_b, series=series)
        
