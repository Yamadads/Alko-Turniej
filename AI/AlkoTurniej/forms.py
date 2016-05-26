from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from registration.forms import RegistrationForm
from .models import Tournament

from registration.forms import RegistrationForm


# class UserProfileRegistrationForm(RegistrationForm):
#     first_name = forms.CharField(max_length=15, label='First name')
# last_name = forms.CharField(max_length=15, label='Last name')


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'branch', 'organizer', 'date', 'location_latitude',
                  'location_longitude', 'min_participants', 'max_participants', 'deadline']


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['email', 'password']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    username = forms.CharField(max_length=30, widget=forms.TextInput)
    first_name = forms.CharField(max_length=30, widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False

        if commit:
            user.save()

        return user


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']
