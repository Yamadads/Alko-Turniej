import urllib
from django.forms import ModelForm
from django import forms
from .models import Tournament, TournamentParticipant
from django.forms.extras.widgets import SelectDateWidget
from datetime import date


class TournamentForm(ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput, required=True,
                           error_messages={'required': 'To pole jest wymagane'})
    branch = forms.CharField(max_length=50, widget=forms.TextInput, required=True,
                             error_messages={'required': 'To pole jest wymagane'})
    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    deadline = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    min_participants = forms.IntegerField(error_messages={'required': 'To pole jest wymagane'})
    max_participants = forms.IntegerField(error_messages={'required': 'To pole jest wymagane'})
    logo1 = forms.ImageField(required=False)
    logo2 = forms.ImageField(required=False)
    logo3 = forms.ImageField(required=False)

    class Meta:
        model = Tournament
        fields = ['name', 'branch', 'date', 'position', 'min_participants', 'max_participants', 'deadline', 'logo1',
                  'logo3', 'logo3']

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        date = cleaned_data.get("date")
        deadline = cleaned_data.get("deadline")
        if deadline > date:
            raise forms.ValidationError({'deadline': ["Termin rejestracji musi poprzedzać datę turnieju", ]})
        if date < date.today():
            raise forms.ValidationError({'date': ["Nie możesz podać daty z przeszłości", ]})

        min = cleaned_data.get("min_participants")
        max = cleaned_data.get("max_participants")
        if min > 1:
            if ((min & (min - 1)) != 0):
                raise forms.ValidationError({'min_participants': ["Liczba musi być potęgą dwójki", ]})
        else:
            raise forms.ValidationError({'min_participants': ["Liczba musi być większa niż 1", ]})
        if max > 1:
            if ((max & (max - 1)) != 0):
                raise forms.ValidationError({'max_participants': ["Liczba musi być potęgą dwójki", ]})
        else:
            raise forms.ValidationError({'max_participants': ["Liczba musi być większa niż 1", ]})
        if min>max:
            raise forms.ValidationError({'max_participants': ["Maksymalna liczba nie może być mniejsza od minimalnej", ]})
            raise forms.ValidationError({'max_participants': ["Minimalna liczba nie może być większa od maksymalnej", ]})
        return cleaned_data


class SearchForm(forms.Form):
    text = forms.CharField(max_length=150, widget=forms.TextInput, required=False)

    class Meta:
        fields = ['text']

    def as_url_args(self):
        return urllib.urlencode(self.cleaned_data)


class TournamentParticipantForm(ModelForm):
    license_number = forms.IntegerField()
    ranking_position = forms.IntegerField()

    class Meta:
        model = TournamentParticipant
        fields = ['license_number', 'ranking_position']
