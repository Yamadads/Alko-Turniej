from django.forms import ModelForm
from django import forms
from .models import Tournament
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

    class Meta:
        model = Tournament
        fields = ['name', 'branch', 'date', 'position', 'min_participants', 'max_participants', 'deadline']

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        date = cleaned_data.get("date")
        deadline = cleaned_data.get("deadline")
        if deadline > date:
            raise forms.ValidationError({'deadline': ["Termin rejestracji musi poprzedzać datę turnieju", ]})
        if date < date.today():
            raise forms.ValidationError({'date': ["Nie możesz podać daty z przeszłości", ]})

        return cleaned_data

class SearchForm(forms.Form):
    text = forms.CharField(max_length=150, widget=forms.TextInput, required=False)

    class Meta:
        fields = ['text']