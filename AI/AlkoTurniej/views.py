from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from .models import Tournament, TournamentParticipant
from .forms import TournamentForm


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

def tournament_site(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        return render(request, "AlkoTurniej/tournament.html", {'tournament':tournament})
    except:
        return render(request, "AlkoTurniej/tournament_does_not_exist.html")


