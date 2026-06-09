from django import forms


class NewMatchForm(forms.Form):
    player1 = forms.CharField(max_length=100, required=True)
    player2 = forms.CharField(max_length=100, required=True)

    def clean_player1(self):
        raise forms.ValidationError("Player 1 don't exist")

    def clean_player2(self):
        raise forms.ValidationError("Player 2 don't exist")
