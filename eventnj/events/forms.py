from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm



class AddParticipantForm(forms.Form):
    name = forms.CharField(label="Imię ", max_length=255)
    mail = forms.CharField(label="email ", max_length=255)

    # defaultowo required jest false
    accept_rodo = forms.BooleanField()

    # https://www.youtube.com/watch?v=pFMrOpDs4QQ
    # accept_rodo = forms.BooleanField(label='accept rodo', help_text='zaakceptuj warunki rodo')

# modelForm
# https://youtu.be/EX6Tt-ZW0so