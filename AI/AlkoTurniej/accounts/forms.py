from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput, label="Email")

    class Meta:
        fields = ['email']


class ResetPasswordConfirmForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")

    class Meta:
        fields = ['new_password1', 'new_password2']

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("Hasło musi być identyczne")

        return cleaned_data


class ChangePasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")

    class Meta:
        fields = ['email', 'password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("Hasło musi być identyczne")

        return cleaned_data


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['email', 'password']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput, label="Email", required=True,
                             error_messages={'required': 'Proszę podaj adres email',
                                             'unique': 'Ten adres email jest zajęty'})
    username = forms.CharField(max_length=30, widget=forms.TextInput,
                               error_messages={'required': 'Proszę podaj swój nick',
                                               'unique': 'Ten nick jest już zajęty'})
    first_name = forms.CharField(max_length=30, widget=forms.TextInput, required=True, )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.clean_email()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False

        if commit:
            user.save()

        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Ten email jest już w użyciu")
        return data
