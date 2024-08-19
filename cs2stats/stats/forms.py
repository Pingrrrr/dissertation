from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'players', 'team_img_url']  