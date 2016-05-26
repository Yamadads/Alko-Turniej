from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from registration.views import RegistrationView
from .models import Tournament, TournamentParticipant
from .forms import TournamentForm
from registration.signals import user_registered
from django.views.generic import View
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def index(request):
    tournaments = Tournament.objects.order_by("date")
    return render_to_response("AlkoTurniej/home_page.html", {
        'user': request.user,
        'items': tournaments
    }, RequestContext(request))


@login_required()
def my_tournaments(request):
    tournaments = Tournament.objects.order_by("date")
    return render_to_response("AlkoTurniej/my_tournaments.html", {
        'user': request.user,
        'items': tournaments
    }, RequestContext(request))


@login_required()
def new_tournament(request):
    return render_to_response("AlkoTurniej/new_tournament.html", {
        'user': request.user,
    }, RequestContext(request))


@login_required()
def new_tournament_form(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/')
            except:
                pass
    return render_to_response('AlkoTurniej/new_tournament.html', {'form': TournamentForm()},
                              context_instance=RequestContext(request))


class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return render(request, "registration/login.html")
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
