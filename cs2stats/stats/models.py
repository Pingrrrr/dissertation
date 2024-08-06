from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    players = models.ManyToManyField('Player', related_name='player_team')
    team_img_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    nick_name = models.CharField(max_length=100, default='Unknown Nickname')
    real_name = models.CharField(max_length=100, default='Unknown Real Name')
    nationality = models.CharField(max_length=50, default='Unknown Nationality')
    age = models.IntegerField(default=0)
    bio = models.TextField(default='No biography available.')
    image_url = models.URLField(blank=True, default='')  # Empty default for blank field
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    steam_id = models.CharField(max_length=50, default='Unknown Steam ID')

    def __str__(self):
        return self.nick_name

class Series(models.Model):
    winningTeam = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return f"{self.id} winner is {self.winningTeam}"
    
    
class Match(models.Model):
    date = models.DateTimeField()
    team_a = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team_a_matches', null=True, blank=True)
    team_b = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='team_b_matches',null=True, blank=True)
    map = models.CharField(max_length=100, default='Unknown')
    series_id = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"
    
class Round(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    round_num = models.IntegerField(default=1)
    isWarmup = models.BooleanField(default=False)
    winningSide = models.CharField(max_length=100, default='Unknown')
    roundEndReason = models.CharField(max_length=100,  default='Unknown') #bomb detonation, T victory, CT victory, defuse

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
    distance = models.FloatField()
    isTrade = models.BooleanField()
    weapon = models.CharField(max_length=100,null=True,default='Unknown')
    weaponClass = models.CharField(max_length=100,null=True, default='Unknown') #this will be table later

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

