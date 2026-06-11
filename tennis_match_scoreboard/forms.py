from django import forms
from .models import Players

class NewMatchForm(forms.Form):
    player1 = forms.CharField(max_length=100, required=True)
    player2 = forms.CharField(max_length=100, required=True)

    def clean_player1(self):
        name = self.cleaned_data['player1']
        try:
            Players.objects.get(**{"name": name})
        except Players.DoesNotExist:
            raise forms.ValidationError("Player one doesn't exist")

    def clean_player2(self):
        name = self.cleaned_data['player2']
        try:
            Players.objects.get(**{"name": name})
        except Players.DoesNotExist:
            raise forms.ValidationError("Player two doesn't exist")
