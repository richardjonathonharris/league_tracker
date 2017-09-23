from django import forms
from django.core.exceptions import ValidationError
from league_tracker.models import User, Decks, Records, Event
import requests

def get_faction_dictionary():
    r = requests.get('https://netrunnerdb.com/api/2.0/public/cards')
    payload = r.json()['data']
    runner_vals = {}
    corp_vals = {}
    for card in payload:
        if card['type_code'] == 'identity':
            if card['side_code'] == 'corp':
                corp_vals[card['title']] = card['faction_code']
            else:
                runner_vals[card['title']] = card['faction_code']
    return runner_vals, corp_vals

class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['name']

class DeckForm(forms.ModelForm):
    runner_vals, corp_vals = get_faction_dictionary()
    runner_choices = [(x, x) for x in sorted(runner_vals.keys())]
    corp_choices = [(x, x) for x in sorted(corp_vals.keys())]
    runner_id = forms.ChoiceField(choices=runner_choices)
    corp_id = forms.ChoiceField(choices=corp_choices)
    class Meta:
        model = Decks
        fields = ['user_id', 'game', 'runner_id', 'corp_id']

class RecordForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=User.objects, empty_label=None)
    opponent_id = forms.ModelChoiceField(queryset=User.objects, empty_label=None)
    game = forms.ModelChoiceField(queryset=Event.objects.order_by('-date'), empty_label=None)
    class Meta:
        model = Records
        fields = ['user_id', 'opponent_id', 'corp_status',
                'runner_status', 'game', 'round_num']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
