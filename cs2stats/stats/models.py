from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    players = models.ManyToManyField('Player', related_name='player_team')
    team_img_url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name
    



class Player(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=100, default='Unknown Nickname')
    real_name = models.CharField(max_length=100, default='Unknown Real Name')
    nationality = models.CharField(max_length=50, default='Unknown Nationality')
    age = models.IntegerField(default=0)
    bio = models.TextField(default='No biography available.')
    image_url = models.URLField(blank=True, default='')  
    steam_id = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.nick_name

class Series(models.Model):
    winningTeam = models.CharField(max_length=100, default='Unknown')
    bestOf = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.id} winner is {self.winningTeam}"
    
class Match(models.Model):
    date = models.DateTimeField()
    team_a = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team_a_matches', null=True, blank=True)
    team_b = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team_b_matches',null=True, blank=True)
    map = models.CharField(max_length=100, default='Unknown')
    series_id = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)
    tick_rate = models.IntegerField(default=64)

    def __str__(self):
        return f"{self.map} : {self.team_a} vs {self.team_b}"
    
class Round(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    round_num = models.IntegerField(default=1)
    isWarmup = models.BooleanField(default=False)
    winningSide = models.CharField(max_length=100, default='Unknown')
    winningTeam = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    roundEndReason = models.CharField(max_length=100,  default='Unknown') #bomb detonation, T victory, CT victory, defuse
    bombPlant = models.BooleanField(default=False)
    t_startEquipmentValue = models.IntegerField(default=0)
    ct_startEquipmentValue = models.IntegerField(default=0)
    t_endEquipmentValue = models.IntegerField(default=0)
    ct_endEquipmentValue = models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.id}"
    
class BombEvent(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=False)
    event = models.CharField(max_length=50)
    site = models.CharField(max_length=50)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)
    ticks_since_round_start	= models.IntegerField(default=0)
    ticks_since_freeze_time_end	= models.IntegerField(default=0)
    ticks_since_bomb_plant	= models.IntegerField(default=0, null=True)
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"
    
    
class Kills(models.Model):
    round_ID = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True, blank=True)
    attacker_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='attacker', null=True, blank=True)
    assister_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='assister', null=True, blank=True)
    victim_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='victim', null=True, blank=True)
    attackerSide = models.CharField(max_length=100,null=True, default='Unknown')
    victimSide = models.CharField(max_length=100,null=True,default='Unknown')
    isHeadshot = models.BooleanField()
    distance = models.FloatField(default=0.0)
    traded_by = models.IntegerField(null=True, default=None)
    weapon = models.CharField(max_length=100,null=True,default='Unknown')
    weaponClass = models.CharField(max_length=100,null=True, default='Unknown') #this will be table later
    tick = models.IntegerField(default=0)
    round_time = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}"
    

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    kills_per_round = models.FloatField(default=0.0)
    deaths_per_round = models.FloatField(default=0.0)
    kd_ratio = models.FloatField(default=0.0)
    headshot_percentage = models.FloatField(default=0.0)
    total_kills = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)
    damage_per_round = models.FloatField(default=0.0)
    rounds_played = models.IntegerField(default=0)
    maps_played = models.IntegerField(default=0)
    win_percentage = models.FloatField(default=0.0)
    entry_kills = models.IntegerField(default=0)
    adr = models.FloatField(default=0.0)
    kast = models.FloatField(default=0.0) 
    impact = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.id}"
    
class Strategy(models.Model):
    name = models.CharField(max_length=100, default='Tactic A')
    description = models.CharField(max_length=100)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE)
    maps = models.ManyToManyField('Map', related_name='map_name')
    rounds = models.ManyToManyField('Round', related_name='round_id')
    type = models.ManyToManyField('StrategyType', related_name='type_id')
    

    def __str__(self):
        return f"{self.tactic_name} "

class StrategyType(models.Model):
    name = models.CharField(max_length=100)
    success_criteria = models.CharField(max_length=1000) # this will eventually be filters on what stats are important like kills, round wins, bobm plants etc
    
class Map(models.Model):
    name = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.map_name}"
    
class SeriesReview(models.Model):
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    created_time = models.DateTimeField()
    last_updated = models.DateTimeField() #can this content be updated by different users and how will i keep track of changes

    def __str__(self):
        return f"{self.series_id}"
    
class SeriesReviewComment(models.Model):
    series_review_id = models.ForeignKey(SeriesReview, on_delete=models.CASCADE)
    comment = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    replay_time_code = models.TimeField()# the time in the replay this comment is talking about (can be left null)
    created_time = models.DateTimeField()
    last_updated = models.DateTimeField() #can this content be updated by different users and how will i keep track of changes

    def __str__(self):
        return f"{self.series_review_id}"



