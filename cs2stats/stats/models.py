from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    players = models.ManyToManyField('Player', related_name='teams_set')
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
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='players_set', null=True, blank=True)
    steam_id = models.CharField(max_length=50, default='Unknown Steam ID')

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

    def __str__(self):
        return self.nick_name
    

class Match(models.Model):
    date = models.DateTimeField()
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField()
    deaths = models.IntegerField()

    def __str__(self):
        return self.name
