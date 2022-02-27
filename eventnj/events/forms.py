from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm


class AddParticipantForm(forms.Form):
    name = forms.CharField(label="Imię ", max_length=255)
    mail = forms.CharField(label="email ", max_length=255)

    # defaultowo required jest false
    accept_rodo = forms.BooleanField()

    def send_email(self):
        #  czy ciało funkcji musi być w forms-ie
        #  jakie to ma konsekwencje?
        #  https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView
        pass

    # https://www.youtube.com/watch?v=pFMrOpDs4QQ
    # accept_rodo = forms.BooleanField(label='accept rodo', help_text='zaakceptuj warunki rodo')

# modelForm
# https://youtu.be/EX6Tt-ZW0so