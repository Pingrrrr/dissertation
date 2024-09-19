from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    tagged_players = models.ManyToManyField('Player', related_name='tagged_in_comments', blank=True)
    acknowledgements = models.ManyToManyField('Player', related_name='acknowledged_by', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created_time']


class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    players = models.ManyToManyField('Player', related_name='player_team')
    team_img_url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=100, null=True)
    real_name = models.CharField(max_length=100, null=True)
    nationality = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0)
    bio = models.TextField(default='No biography available.')
    image_url = models.URLField(blank=True, default='')  
    steam_id = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.nick_name

class Series(models.Model):
    title = models.TextField(default='Series')

    def __str__(self):
        return self.title
    
class Lineup(models.Model):
    clanName = models.CharField(max_length=100, default='Unknown')
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    players = models.ManyToManyField(Player, related_name='player_lineup')


class Match(models.Model):
    date = models.DateTimeField()
    teams = models.ManyToManyField(Team, related_name='teams')
    team_a_lineup = models.ForeignKey(Lineup, on_delete=models.SET_NULL, related_name='team_a_lineup', null=True)
    team_b_lineup = models.ForeignKey(Lineup, on_delete=models.SET_NULL, related_name='team_b_lineup', null=True)
    map = models.CharField(max_length=100, default='Unknown')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    tick_rate = models.IntegerField(default=64)

    def __str__(self):
        return f"{self.map} : {self.team_a_lineup.clanName} vs {self.team_b_lineup.clanName}"
    
    
class Round(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    round_num = models.IntegerField(default=1)
    isWarmup = models.BooleanField(default=False)
    winningSide = models.CharField(max_length=100, default='Unknown')
    winningTeam = models.ForeignKey(Lineup, on_delete=models.SET_NULL, null=True)
    roundEndReason = models.CharField(max_length=100,  default='Unknown') #bomb detonation, T victory, CT victory, defuse
    bombPlant = models.BooleanField(default=False)
    t_startEquipmentValue = models.IntegerField(default=0)
    ct_startEquipmentValue = models.IntegerField(default=0)
    t_endEquipmentValue = models.IntegerField(default=0)
    ct_endEquipmentValue = models.IntegerField(default=0)
    ticks = models.JSONField(null=True)
    post = models.OneToOneField(Post, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.id}"
    
class PlayerTick(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=False)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    side = models.CharField(max_length=25)
    tick = models.IntegerField(null=False)
    health = models.FloatField(null=False)
    armor_value = models.FloatField(null=True, default=0.0)
    x= models.FloatField(default=0.0)
    y= models.FloatField(default=0.0)
    z= models.FloatField(default=0.0)
    yaw = models.FloatField(default=0.0)
    inventory = models.CharField(max_length=500)
    current_equip_value = models.FloatField(default=0.0)
    flash_duration = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.player.id} : {self.tick}"

    
class BombEvent(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=False)
    event = models.CharField(max_length=50)
    site = models.CharField(max_length=50)
    tick = models.IntegerField(default=0)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)
    ticks_since_round_start	= models.IntegerField(default=0)
    ticks_since_freeze_time_end	= models.IntegerField(default=0)
    ticks_since_bomb_plant	= models.IntegerField(default=0, null=True)
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"
    
class Grenade(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=False)
    thrower = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True)
    thrower_name = models.CharField(max_length=250)
    grenade_type = models.CharField(max_length=25)
    tick = models.IntegerField(default=0)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)

class WeaponFires(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=False)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    side = models.CharField(max_length=25)
    tick = models.IntegerField(default=0)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)
    yaw = models.FloatField(default=0.0)
    weapon = models.CharField(max_length=250)
    zoom_level = models.FloatField(default=0.0)
    accuracy_penalty = models.FloatField(default=0.0)
    

    
class Kills(models.Model):
    round_ID = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True, blank=True)
    attacker_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='attacker', null=True, blank=True)
    attackerX = models.FloatField(default=0.0)
    attackerY = models.FloatField(default=0.0)
    attackerZ = models.FloatField(default=0.0)
    assister_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='assister', null=True, blank=True)
    assisterX = models.FloatField(default=0.0)
    assisterY = models.FloatField(default=0.0)
    assisterZ = models.FloatField(default=0.0)
    victim_ID = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='victim', null=True, blank=True)
    victimX = models.FloatField(default=0.0)
    victimY = models.FloatField(default=0.0)
    victimZ = models.FloatField(default=0.0)
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
    side = models.CharField(max_length=24, null=True)
    rating = models.FloatField(default=0.0)
    kills_per_round = models.FloatField(default=0.0)
    deaths_per_round = models.FloatField(default=0.0)
    kd_ratio = models.FloatField(default=0.0)
    headshot_percentage = models.FloatField(default=0.0)
    total_kills = models.IntegerField(default=0)
    total_assists = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)
    damage_per_round = models.FloatField(default=0.0)
    rounds_played = models.IntegerField(default=0)
    adr = models.FloatField(default=0.0)
    kast = models.FloatField(default=0.0) 
    impact = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.id}"
    
class Strategy(models.Model):
    name = models.CharField(max_length=100, default='Tactic A')
    description = models.CharField(max_length=10000)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE)
    stratCanvas = models.JSONField(null=True)
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
    

class Notification(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    round = models.ForeignKey('Round', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

class UploadedDemo(models.Model):
    hash = models.CharField(primary_key=True, max_length=64, default="")
    match = models.ForeignKey(Match, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self} "
    
class UploadedDemoFile(models.Model):
    demo = models.ForeignKey(UploadedDemo, on_delete=models.SET_NULL, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='demos/', validators=[FileExtensionValidator(allowed_extensions=['dem'])])
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='unknown')
    options = models.JSONField(null=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.uploaded_by} "



