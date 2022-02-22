from django import forms
from django.core.exceptions import ValidationError


class addParticipantForm(forms.Form):
    name = forms.CharField(label="Imię ", max_length=255)
    mail = forms.CharField(label="email ", max_length=255)

