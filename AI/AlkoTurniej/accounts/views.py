from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from .models import UserActivations
from django.conf import settings
import datetime
from django.utils import timezone


class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    @transaction.atomic
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            current_site = settings.BASE_URL
            send_activation_email(user, current_site)
            return render(request, "registration/registration_complete.html")
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'registration/login.html'
    template_invalid_name = 'registration/login_invalid.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "registration/activate.html")
        return render(request, self.template_invalid_name, {'form': form})


def logout_view(request):
    logout(request)
    return render(request, "registration/logout.html")


def send_activation_email(user, site):
    activation = UserActivations.objects.create(user=user)
    activation.set_activation_key(user.email)
    activation.save()
    ctx_dict = {'activation_key': activation.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'user': user,
                'site': site}
    subject = render_to_string('registration/activation_email_subject.txt', ctx_dict)
    subject = ''.join(subject.splitlines())

    message = render_to_string('registration/activation_email.txt', ctx_dict)

    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def activate_view(request, activation_key_link):
    activations = UserActivations.objects.filter(activation_key=activation_key_link).first()
    if activations is not None:
        if not activation_expired(activations.user):
            user = activations.user
            user.is_active = True
            user.save()
            UserActivations.objects.get(activation_key=activation_key_link).delete()
            return render(request, "registration/activation_complete.html")
        activations.user.delete()
        activations.delete()
    return render(request, "registration/activation_key_expired.html")


def activation_expired(user):
    expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    return (user.date_joined + expiration_date <= timezone.now())

class ChangePasswordView(View):
    form_class = ChangePasswordForm
    template_name = 'registration/password_change_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     username = request.POST['email']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return HttpResponseRedirect(reverse('index'))
    #         else:
    #             return render(request, "registration/activate.html")
    #     return render(request, self.template_invalid_name, {'form': form})