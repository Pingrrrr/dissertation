#https://stackoverflow.com/a/24456404
import datetime
import json
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs2stats.settings")
django.setup()
from django.shortcuts import get_object_or_404
from django.utils import timezone
from awpy import Demo
from stats.models import Player, Match, Stat, Team, Series, Round, Kills
#https://docs.djangoproject.com/en/5.0/ref/exceptions/
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from stats.demo import getPlayerPositions, determineTickRate



dem = Demo(r"media\demos\complexity-vs-natus-vincere-m2-nuke.dem", ticks=True)

pos = getPlayerPositions(dem, 2, determineTickRate(dem))
pos['playerPositions']=pos['playerPositions'][403:404]
pos['grenades']=pos['grenades'][403:404]
pos['weaponFires']=pos['weaponFires'][403:404]
print(len(pos['playerPositions']))
print(len(pos['grenades']))
print(len(pos['weaponFires']))
print(json.dumps(pos, indent=4))
#    return {"playerPositions":playerPos, "grenades":grenades, "weaponFires":weaponFires}
#print(getPlayerPositions(dem, 1, determineTickRate(dem)))


#r=Round.objects.get(id=133)
#r.ticks=pos
#r.save()

