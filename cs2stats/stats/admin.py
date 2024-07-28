from django.contrib import admin
from .models import Player, Match, Stat, Team

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Stat)
