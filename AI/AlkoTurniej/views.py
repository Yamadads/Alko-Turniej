from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
import datetime
from django.db.models import Q
from operator import and_, or_
from functools import reduce
import re


class Index(View):
    form_class = SearchForm
    tournaments = Tournament.objects.order_by("-date").exclude(date__lte=datetime.date.today())

    def get(self, request):
        form = self.form_class(initial={'text': 'Nazwa turnieju ; dyscyplina ; organizator ; data'})
        if 'search_text' in request.session:
            search_string = request.session['search_text']
            form = self.form_class(initial={'text': search_string })
            array_search = re.split('\s*;\s*', search_string)
            if len(array_search) > 0:
                self.tournaments = Tournament.objects.filter(
                    reduce(and_, [Q(organizer__username__icontains=a) |
                                  Q(name__icontains=a) |
                                  Q(branch__icontains=a) |
                                  Q(date__icontains=a) for a in array_search])
                ).exclude(date__lte=datetime.date.today())
        paginator = Paginator(self.tournaments, 10)
        page = request.GET.get('page')
        try:
            tournaments_list = paginator.page(page)
        except PageNotAnInteger:
            tournaments_list = paginator.page(1)
        except EmptyPage:
            tournaments_list = paginator.page(paginator.num_pages)
        return render_to_response("AlkoTurniej/home_page.html", {
            'user': request.user,
            'items': tournaments_list,
            'form': form
        }, RequestContext(request))

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data['text']
            array_search = re.split('\s*;\s*', search_string)
            if len(array_search) > 0:
                self.tournaments = Tournament.objects.filter(
                    reduce(and_, [Q(organizer__username__icontains=a) |
                                  Q(name__icontains=a) |
                                  Q(branch__icontains=a) |
                                  Q(date__icontains=a) for a in array_search])
                ).exclude(date__lte=datetime.date.today())
        paginator = Paginator(self.tournaments, 10)
        tournaments_list = paginator.page(1)
        request.session['search_text'] = search_string
        return render_to_response("AlkoTurniej/home_page.html", {
            'user': request.user,
            'items': tournaments_list,
            'form': form
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
