from django import forms
from django.core.exceptions import ValidationError

class NewMatchForm(forms.Form):
    player1 = forms.CharField(max_length=100, required=True)
    player2 = forms.CharField(max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['player1'] == cleaned_data['player2']:
            raise ValidationError("Players must have different names.")
        return cleaned_data
