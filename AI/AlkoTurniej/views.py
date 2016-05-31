from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.generic import View
from .models import Tournament, TournamentParticipant
from .forms import TournamentForm, SearchForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Index(View):
    form_class = SearchForm

    def get(self,request):
        form = self.form_class(None)
        tournaments = Tournament.objects.order_by("date")
        return render_to_response("AlkoTurniej/home_page.html", {
            'user': request.user,
            'items': tournaments,
            'form':form
        }, RequestContext(request))


@login_required()
def my_tournaments_organizer(request):
    tournaments = Tournament.objects.filter(organizer=request.user).order_by("date")
    return render_to_response("AlkoTurniej/my_tournaments_organizer.html", {
        'user': request.user,
        'items': tournaments
    }, RequestContext(request))


@login_required()
def my_tournaments_participant(request):
    user_participant = [i.tournament for i in TournamentParticipant.objects.filter(participant=request.user)]
    tournaments = Tournament.objects.filter(organizer=request.user).order_by("date")
    tournaments = [i for i in tournaments if i in user_participant]
    return render_to_response("AlkoTurniej/my_tournaments_participant.html", {
        'user': request.user,
        'items': tournaments
    }, RequestContext(request))


class NewTournament(View):
    form_class = TournamentForm

    def get(self, request):
        form = self.form_class(None)
        if request.user.is_authenticated():
            return render(request, "AlkoTurniej/new_tournament.html", {
                'user': request.user,
                'form': form
            }, RequestContext(request))
        return HttpResponseRedirect(reverse('auth_login'))

    def post(self, request):
        form = self.form_class(request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                tournament = form.save(commit=False)
                tournament.organizer = request.user
                tournament.save()
                return HttpResponseRedirect(reverse('my_tournaments_organizer'))
            return render(request, "AlkoTurniej/new_tournament.html", {
                'user': request.user,
                'form': form
            }, RequestContext(request))
        return HttpResponseRedirect(reverse('auth_login'))


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


def tournament_site(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        organizer = User.objects.get(username=tournament.organizer)
        return render(request, "AlkoTurniej/tournament.html",
                      {
                          'tournament': tournament,
                          'organizer': organizer
                      })
    except:
        return render(request, "AlkoTurniej/tournament_does_not_exist.html")
