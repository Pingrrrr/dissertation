from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team, UploadedDemoFile,Series, Comment, Player, Strategy, Match
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
    file=forms.FileField()
    description=forms.CharField(required=False)
    series_id=forms.ModelChoiceField(queryset=Series.objects.none(), empty_label="Create new series", required=False)
    link_team = forms.BooleanField(required=False, initial=True, label="Link my team to this match")
    match_date = forms.DateField(widget=forms.SelectDateWidget)


    class Meta:
        model = UploadedDemoFile
        fields = ['file', 'description', 'series_id']  



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'tagged_players', 'parent']
        widgets = {'parent':forms.HiddenInput, 'tagged_players':forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)

        super().__init__(*args, **kwargs)
        self.fields['tagged_players'].label = 'Tag player'
        if team:
            self.fields['tagged_players'].queryset = Player.objects.filter(player_team=team)

class EditSeriesForm(forms.ModelForm):

    matchesToAdd = forms.ModelChoiceField(queryset=Match.objects.all(), empty_label="Add Matches", required=False)
    matchesToRemove = forms.ModelChoiceField(queryset=Match.objects.all(), empty_label="Remove Matches", required=False)

    class Meta:
        model=Series
        fields=['title', 'matchesToAdd', 'matchesToRemove']
        widgets = {'matchesToAdd':forms.CheckboxSelectMultiple, 'title': forms.Textarea(attrs={'rows': 1, 'cols': 40})}
    
    def __init__(self, *args, **kwargs):
        series = kwargs.pop('series', None)

        super().__init__(*args, **kwargs)
        self.fields['matchesToAdd'].label = 'Add Match'
        if series:
            #self.fields['title'].initial = series.title
            self.fields['matchesToAdd'].queryset = Match.objects.all()
            self.fields['matchesToRemove'].queryset = Match.objects.filter(series=series)









