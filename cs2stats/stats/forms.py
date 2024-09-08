from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team, UploadedDemo,Series, Comment, Player, Strategy
from django.db.models import Q




class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'players', 'team_img_url']  

#https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/
class DemoUploadForm(forms.ModelForm):

    class Meta:
        model = UploadedDemo
        fields = ['file', 'description', 'series']  
    # Customizes the form initialization to filter the series field based on the team
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            self.fields['series'].queryset = Series.objects.filter(Q(team_a=team) | Q(team_b=team))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'tagged_players']

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            
            self.fields['tagged_players'].queryset = Player.objects.filter(player_team=team)





