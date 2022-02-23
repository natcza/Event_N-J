from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

class addParticipantForm(forms.Form):
    name = forms.CharField(label="Imię ", max_length=255)
    mail = forms.CharField(label="email ", max_length=255)
    accept_rodo = forms.BooleanField(required=True, error_messages={'required': 'zaakceptuj warunki rodo'})

    # https://www.youtube.com/watch?v=pFMrOpDs4QQ
    # accept_rodo = forms.BooleanField(label='accept rodo', help_text='zaakceptuj warunki rodo')
