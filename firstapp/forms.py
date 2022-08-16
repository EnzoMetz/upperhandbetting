from socket import fromshare
from django import forms
from django.core import validators

PROP_CHOICES=[
    ('points', 'Points'),
    ('rebounds', 'Rebounds'),
    ('assists', 'Assists'),
    ('blocks', 'Blocks'),
    ('steals', 'Steals'),
    ('three-points%20made', '3 Pointers Made'),
]

class DateInput(forms.DateInput):
    input_type = 'date'

def checkInput(value):
    checkForComp = False
    for x in value :
        if ((x == '>') or (x == '<')):
            checkForComp = True

    if (checkForComp == False) :
        raise forms.ValidationError("Expression must evaluate to True or False. Please use '>' or '<' in your answer.")
    

class FormName(forms.Form):
    prop_stat = forms.CharField(label='What prop statistic would you like to show bets for?', 
    widget=forms.Select(choices=PROP_CHOICES))
    date_stat = forms.DateField(label='What day would you like to show matching bets from?', widget=DateInput)
    algorithm_field = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'algorithm_field'}))

    

 
