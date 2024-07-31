#https://stackoverflow.com/a/24456404
import datetime
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs2stats.settings")
django.setup()
from django.utils import timezone
from awpy import Demo
from stats.models import Player, Match, Stat, Team, Series, Round, Kills


#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem")
dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem", ticks=False)


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
#for kill in dem.kills:
    #this is not optimal, prob best storing 10 players steamid at the start once rather than querying the db
    round = Round.objects.get(id=kill['round'])
    attacker = Player.objects.get(steam_id=kill['attacker_steamid'])
    assister = Player.objects.filter(steam_id=kill['assister_steamid'])
    victim = Player.objects.get(steam_id=kill['victim_steamid'])
    
    k = Kills(round_ID = round, attacker_ID = attacker, victim_ID = victim, attackerSide = kill['attacker_team_name'], 
              victimSide = kill['victim_team_name'], isHeadshot = kill['headshot'], distance = 0.0, isTrade = False, weapon = kill['weapon'], weaponClass = "weapons" )
    if  assister:
        k.assister_ID = assister[0]
    k.save()