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


#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem")
dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem", ticks=True)


#dem = parser.parse()

# Available properties (all demos)
print(dem.kills[["attacker_name", "attacker_steamid","assister_name", "assister_steamid","victim_name", "victim_steamid"]].sample(n=100))
#print(f"Kills: \n{dem.kills["attacker_name", "attacker_steamid","assister_name", "assister_steamid","victim_name", "victim_steamid" ].sample(n=100)}")
#print(f"\nDamages: \n{dem.damages.head(n=3)}")
#print(f"\nBomb: \n{dem.bomb.head(n=3)}")
#print(f"\nSmokes: \n{dem.smokes.head(n=3)}")
#print(f"\nInfernos: \n{dem.infernos.head(n=3)}")
#print(f"\nWeapon Fires: \n{dem.weapon_fires.head(n=3)}")
#print(f"\nRounds: \n{dem.rounds.head(n=3)}")
#print(f"\nGrenades: \n{dem.grenades.head(n=3)}")
#print(f"\nTicks: \n{dem.ticks.head(n=3)}")

#print(f"\nHeader: \n{dem.header}")

print(dem.header['map_name'])
#print(type(dem.header))

#series 1
series = Series.objects.get(id=1)
navi = Team.objects.get(id=1)
vp = Team.objects.get(id=2)
match = Match.objects.get(id=1)
#can also query like this: https://docs.djangoproject.com/en/5.0/topics/db/queries/#retrieving-objects


#match
#match = Match()
#match.date=timezone.now()

#match.team_a=navi
#match.team_b=vp
#match.map = dem.header['map_name']
#match.series_id = series
#match.save()



#round

#for index, round in dem.rounds.iterrows():
#for round in dem.rounds:
#    print(round)
#    print(type(round))
#    r=Round(match_id=match, round_num=round['round'], isWarmup=False, winningSide=round['winner'], roundEndReason=round['reason'])
#    r.save()

#kills



for index, kill in dem.kills.iterrows():
    # if it doesn't exist, print a message and skip to the next kill.
    try:
        round_ID = Round.objects.get(id=kill['round'])
    except ObjectDoesNotExist:
        print(f"Round with id {kill['round']} does not exist")
        continue
    
    # Try-Except / If any of them do not exist, print a message and set the variable to None.
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

    
    if round_ID:
        k = Kills(
            round_ID=round_ID, 
            attackerSide=kill['attacker_team_name'], 
            victimSide=kill['victim_team_name'], 
            isHeadshot=kill['headshot'], 
            distance=0.0, 
            isTrade=False, 
            weapon=kill['weapon'], 
            weaponClass="weapons"
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


adr_stats = adr(dem)
kast_stats = kast(dem)
rating_stats = rating(dem)


match_id = 1  
match = Match.objects.get(id=match_id)


print(dem.kills.columns)


player_steam_ids = set(dem.kills['attacker_steamid']).union(set(dem.kills['victim_steamid']))
for steam_id in player_steam_ids:
    
    try:
        player_instance = Player.objects.get(steam_id=steam_id)
    except Player.DoesNotExist:
        print(f"Player with steam_id {steam_id} does not exist")
        continue

    
    total_kills = len(dem.kills[dem.kills['attacker_steamid'] == steam_id])
    total_deaths = len(dem.kills[dem.kills['victim_steamid'] == steam_id])
    rounds_played = len(dem.rounds)

    if rounds_played > 0:
        kills_per_round = total_kills / rounds_played
        deaths_per_round = total_deaths / rounds_played
        kd_ratio = total_kills / (total_deaths if total_deaths > 0 else 1)
        damage_per_round = adr_stats.get(steam_id, 0)
        headshot_percentage = (dem.kills[dem.kills['attacker_steamid'] == steam_id]['headshot'].mean()) * 100
        
        # Adjust the column names based on inspection
        try:
            win_percentage = (dem.rounds[dem.rounds['winning_side'] == player_instance.team.name].shape[0] / rounds_played) * 100
        except KeyError:
            win_percentage = 0  # Set a default value or handle as needed

        try:
            
            entry_kills = len(dem.kills[(dem.kills['attacker_steamid'] == steam_id) & (dem.kills['is_entry'] == True)])
        except KeyError:
            entry_kills = 0  # Set a default value or handle as needed
        
        adr_value = adr_stats.get(steam_id, 0)
        kast_value = kast_stats.get(steam_id, 0)
        impact_value = rating_stats.get(steam_id, 0)
        
        
        stat, created = Stat.objects.update_or_create(
            player=player_instance,
            match=match,
            defaults={
                'rating': rating_stats.get(steam_id, 0),
                'kills_per_round': kills_per_round,
                'deaths_per_round': deaths_per_round,
                'kd_ratio': kd_ratio,
                'headshot_percentage': headshot_percentage,
                'total_kills': total_kills,
                'total_deaths': total_deaths,
                'damage_per_round': damage_per_round,
                'rounds_played': rounds_played,
                'maps_played': 1,  # Assuming 1 map per match for simplicity
                'win_percentage': win_percentage,
                'entry_kills': entry_kills,
                'adr': adr_value,
                'kast': kast_value,
                'impact': impact_value
            }
        )

        print(f"Updated stats for player {player_instance.nick_name}")
        
