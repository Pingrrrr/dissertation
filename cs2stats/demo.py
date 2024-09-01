#https://stackoverflow.com/a/24456404
import datetime
import json
import MySQLdb
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs2stats.settings")
django.setup()
from django.utils import timezone
from awpy import Demo
from stats.models import Grenade, Player, Match, PlayerTick, Stat, Team, Series, Round, Kills, BombEvent, WeaponFires
#https://docs.djangoproject.com/en/5.0/ref/exceptions/
from django.core.exceptions import ObjectDoesNotExist
from awpy.stats import adr
from awpy.stats import kast
from awpy.stats import rating
from django.db.models import Q
import pandas as pd


def determineTickRate(demo):
    t=demo.ticks[['game_time', 'tick']].sample(n=2)
    tickDiff = t.iloc[1]['tick']-t.iloc[0]['tick']
    timeDiff = t.iloc[1]['game_time']-t.iloc[0]['game_time']
    return round(tickDiff/timeDiff)

def determineTrades(match, tradeTime, tickRate):
    for round in match.round_set.all():
        for kill in round.kills_set.all():
            #find kills from the last few seconds
            prevKills = round.kills_set.filter(tick__lt=kill.tick).filter(tick__gt=kill.tick-(tradeTime*tickRate))

            #if the victim of this kill was the attacker of a recent kill, we can mark that previous kill as a trade
            if prevKills.filter(attacker_ID=kill.victim_ID).exists():
                #only the most recent kill will get marked as traded so we dont allow a player to get traded more than once
                prevKill = prevKills.filter(attacker_ID=kill.victim_ID).order_by('-tick')[:1]
                pk = Kills.objects.get(id=prevKill)
                pk.tradedBy = kill.id
                pk.save()
                print(f"Round {round.round_num} : {pk.victim_ID} was traded by {kill.id}")


players={}
def getPlayer(steamId):
    if steamId in players.keys():
        return players[steamId]
    else:
        try:
            player = Player.objects.get(steam_id=steamId)
            players[steamId] = player
        except Player.DoesNotExist:
            print(f"Player with steam_id {steamId} not found")
            return None



def getPlayerPositions(dem, roundNum, tickRate):
    roundTicks = dem.ticks[dem.ticks['round']==roundNum].sort_values(by=['tick'])
    grenadeTicks = dem.grenades[dem.grenades['round']==roundNum].sort_values(by=['tick'])
    tickPrecision = round(tickRate/4) #dont need to store full tick rate (usually 64 ticks per second)

    weaponFiresTicks = dem.weapon_fires[dem.weapon_fires['round']==roundNum]
    weaponFiresTicks = weaponFiresTicks[['player_steamid','player_name','tick','player_X','player_Y','player_Z','player_yaw','weapon','player_accuracy_penalty']]


    startTick = roundTicks.head(1)['tick'].values[0]
    endTick = roundTicks.tail(1)['tick'].values[0]
    ticks = list(range(startTick,endTick, tickPrecision)) 
    roundTicks = roundTicks[roundTicks['tick'].isin(ticks)]
    grenadeTicks = grenadeTicks[grenadeTicks['tick'].isin(ticks)]
    playerPos=[]
    grenades=[]
    weaponFires=[]

    lastTick = 0
    for tick in ticks:
        roundTick = roundTicks[roundTicks['tick']==tick][['tick','steamid','name','X','Y', 'health', 'armor_value','yaw', 'inventory', 'team_name']]
        t=[]
        for i in roundTick.index:
            t.append(roundTick.loc[i].to_dict())

        grenadeTick = grenadeTicks[grenadeTicks['tick']==tick][['entity_id','tick','thrower_steamid','thrower','grenade_type','X','Y','Z']]
        grenadesTick=[]
        for g in grenadeTick.index:
            grenadesTick.append(grenadeTick.loc[g].to_dict())

        weaponFiresTick = weaponFiresTicks[(weaponFiresTicks['tick']<=tick) & (weaponFiresTicks['tick']>lastTick)]
        ww=[]
        for w in weaponFiresTick.index:
            ww.append(weaponFiresTick.loc[w].to_dict())


        playerPos.append(t)
        grenades.append(grenadesTick)
        weaponFires.append(ww)
        lastTick = tick
    

    return {"playerPositions":playerPos, "grenades":grenades, "weaponFires":weaponFires}

def processPlayerTicks(dem, match):
    print("Processing player ticks")
    player_ticks = []
    for index, tick in dem.ticks.iterrows():
        try:
            round = Round.objects.filter(match_id=match).get(round_num=tick['round'])
        except ObjectDoesNotExist:
            print(f"round_num {tick['round']} does not exist for match {match}")
            continue
        try:
            player = Player.objects.get(steam_id=tick['steamid'])
        except Player.DoesNotExist:
            print(f"Attacker with steam_id {tick['steamid']} does not exist")
            player = None
        
        pt = PlayerTick(
            round=round,
            player = player,
            name = tick['name'],
            side = tick['team_name'],
            tick = tick['tick'],
            health = tick['health'],
            armor_value = tick['armor_value'],
            x= tick['X'],
            y= tick['Y'],
            z= tick['Z'],
            yaw = tick['yaw'],
            inventory = tick['inventory'],
            current_equip_value = tick['current_equip_value'],
            flash_duration = tick['flash_duration']
            )

        player_ticks.append(pt)
    PlayerTick.objects.bulk_create(player_ticks)

def processGrenades(dem, round):
    print(f"Processing grenades for round {round.round_num}")
    grenades = []
    for index, grenade in dem.grenades.iterrows():
        player = getPlayer(grenade['thrower_steamid'])
        
        g = Grenade(
            round=round,
            thrower = player,
            thrower_name = grenade['thrower'],
            grenade_type = grenade['grenade_type'],
            tick = grenade['tick'],
            x = grenade['X'],
            y = grenade['Y'],
            z = grenade['Z'],
            )

        grenades.append(g)
        print(index)
    Grenade.objects.bulk_create(grenades)

def processWeaponFires(dem, match):
    print("Processing weapon fires")
    weapon_fires = []
    for index, fire in dem.weapon_fires.iterrows():
        try:
            round = Round.objects.filter(match_id=match).get(round_num=fire['round'])
        except ObjectDoesNotExist:
            print(f"round_num {fire['round']} does not exist for match {match}")
            continue
        try:
            player = Player.objects.get(steam_id=fire['player_steamid'])
        except Player.DoesNotExist:
            print(f"Attacker with steam_id {fire['player_steamid']} does not exist")
            player = None
        
        wf = WeaponFires(
            round = round,
            player = player,
            name = fire['player_name'],
            side = fire['player_team_name'],
            tick = fire['tick'],
            x = fire['player_X'],
            y = fire['player_Y'],
            z = fire['player_Z'],
            yaw = fire['player_yaw'],
            weapon = fire['weapon'],
            zoom_level = fire['player_zoom_lvl'],
            accuracy_penalty = fire['player_accuracy_penalty'],
            )

        weapon_fires.append(wf)
    WeaponFires.objects.bulk_create(weapon_fires)



def parseMatchFromDemo(dem, ctTeam, tTeam, series, tickRate):

    if not series:
        series = Series(winningTeam="Undecided")
        series.save()

    #match
    match = Match()
    match.date=timezone.now()

    match.team_a=ctTeam
    match.team_b=tTeam
    match.map = dem.header['map_name'] 
    match.series = series
    match.tick_rate=tickRate
    match.save()


    #round
    for index, round in dem.rounds.iterrows():


        #for some reason the winner is returned as a number (3=CT, 2=T)
        if (round['winner'] == "CT") or (round['winner'] == 3):
            winner = ctTeam
        else:
            winner = tTeam

        #had to increase the max_allowed_packet in mysql to 100M
        playerPos = getPlayerPositions(dem, round['round'], tickRate)


        r=Round(match_id=match, round_num=round['round'], isWarmup=False, winningSide=round['winner'], winningTeam=winner, roundEndReason=round['reason'], ticks=playerPos)
        r.save()
        #processGrenades(dem, r)


        # use the last round of the half to work out when the teams swap sides (and it even works for overtime)
        if (round['round']-1) in dem.events['round_announce_last_round_half']['round'].tolist():
            tmpCtTeam = ctTeam
            ctTeam = tTeam
            tTeam = tmpCtTeam

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

    determineTrades(match=match, tradeTime=5, tickRate=tickRate)

    #bomb events
    print("Processing bomb events")
    bomb_events = []
    for index, bomb_event in dem.bomb.iterrows():
        try:
            round = Round.objects.filter(match_id=match).get(round_num=bomb_event['round'])
        except ObjectDoesNotExist:
            print(f"round_num {kill['round']} does not exist for match {match}")
            continue
        
        b = BombEvent(
            round=round,
            event=bomb_event['event'],
            site=bomb_event['site'],
            tick=bomb_event['tick'],
            x=bomb_event['X'],
            y=bomb_event['Y'],
            z=bomb_event['Z'],
            ticks_since_round_start = bomb_event['ticks_since_round_start'],
            ticks_since_freeze_time_end	= bomb_event['ticks_since_freeze_time_end'],
            ticks_since_bomb_plant	= bomb_event['ticks_since_bomb_plant'] if not pd.isna(bomb_event['ticks_since_bomb_plant']) else 0,
        )

        bomb_events.append(b)
    BombEvent.objects.bulk_create(bomb_events)

    #player ticks
    #processPlayerTicks(dem, match)
    

    #grenades
    

    #weapon fires
    

    #stats
    print("Processing stats")
    adr_stats = adr(dem)
    kast_stats = kast(dem, trade_ticks=tickRate)
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




dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem", ticks=True)
#dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m2-anubis.dem", ticks=True)


#series 1
#series = Series.objects.get(id=1)
#make a new series


#ct_team = dem.events['begin_new_match'][['ct_team_clan_name']]
#t_team = dem.events['begin_new_match'][['t_team_clan_name']]

team_a = Team.objects.get(id=1) #navi
team_b = Team.objects.get(id=2) #vp

series = Series(team_a=team_a, team_b=team_b, best_of=3)
series.save()

tickRate = determineTickRate(demo=dem)
parseMatchFromDemo(dem=dem, ctTeam=team_a, tTeam=team_b, series=series, tickRate=tickRate)
        
