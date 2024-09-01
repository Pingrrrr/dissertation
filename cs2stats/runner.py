#https://stackoverflow.com/a/24456404
import datetime
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



match = Match.objects.get(id=1)
for round in match.round_set.all():
    for kill in round.kills_set.all():
        #find kills from the last few seconds
        prevKills = round.kills_set.filter(tick__lt=kill.tick).filter(tick__gt=kill.tick-(5*128))

        #if the victim of this kill was the attacker of a recent kill, we can mark that previous kill as a trade
        if prevKills.filter(attacker_ID=kill.victim_ID).exists():
            #only the most recent kill will get marked as traded so we dont allow a player to get traded more than once
            prevKill = prevKills.filter(attacker_ID=kill.victim_ID).order_by('-tick')[:1]
            pk = Kills.objects.get(id=prevKill)
            pk.tradedBy = kill.id
            pk.save()
            print(f"Round {round.round_num} : {pk.victim_ID} was traded by {kill.id}")


