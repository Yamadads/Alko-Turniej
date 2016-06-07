from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.generic import View
from .models import Tournament, TournamentParticipant, Encounter
from .forms import TournamentForm, SearchForm, TournamentParticipantForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
from django.db.models import Q
from operator import and_, or_
from functools import reduce
import re
import json
from math import log, pow


class Index(View):
    form_class = SearchForm
    tournaments = Tournament.objects.order_by("date").exclude(date__lte=datetime.date.today())

    def get(self, request):
        form = self.form_class(initial={'text': 'Nazwa turnieju ; dyscyplina ; organizator ; data'})
        if 'search_text' in request.session:
            search_string = request.session['search_text']
            form = self.form_class(initial={'text': search_string})
            array_search = re.split('\s*;\s*', search_string)
            if len(array_search) > 0:
                self.tournaments = Tournament.objects.filter(
                    reduce(and_, [Q(organizer__username__icontains=a) |
                                  Q(name__icontains=a) |
                                  Q(branch__icontains=a) |
                                  Q(date__icontains=a) for a in array_search])
                ).exclude(date__lte=datetime.date.today()).order_by("date")
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
                ).exclude(date__lte=datetime.date.today()).order_by("date")
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
    tournaments = Tournament.objects.filter(organizer=request.user).order_by("date") \
        .exclude(date__lte=datetime.date.today())
    paginator = Paginator(tournaments, 10)
    page = request.GET.get('page')
    try:
        tournaments_list = paginator.page(page)
    except PageNotAnInteger:
        tournaments_list = paginator.page(1)
    except EmptyPage:
        tournaments_list = paginator.page(paginator.num_pages)
    history = False
    return render_to_response("AlkoTurniej/my_tournaments_organizer.html", {
        'user': request.user,
        'items': tournaments_list,
        'history': history
    }, RequestContext(request))


@login_required()
def my_tournaments_organizer_history(request):
    tournaments = Tournament.objects.filter(organizer=request.user).order_by("-date") \
        .exclude(date__gte=datetime.date.today())
    paginator = Paginator(tournaments, 10)
    page = request.GET.get('page')
    try:
        tournaments_list = paginator.page(page)
    except PageNotAnInteger:
        tournaments_list = paginator.page(1)
    except EmptyPage:
        tournaments_list = paginator.page(paginator.num_pages)
    history = True
    return render_to_response("AlkoTurniej/my_tournaments_organizer.html", {
        'user': request.user,
        'items': tournaments_list,
        'history': history
    }, RequestContext(request))


@login_required()
def my_tournaments_participant(request):
    user_participant = [i.tournament for i in TournamentParticipant.objects.filter(participant=request.user)]
    tournaments = Tournament.objects.order_by("date").filter(date__gte=datetime.date.today())
    tournaments = [i for i in tournaments if i in user_participant]
    paginator = Paginator(tournaments, 10)
    page = request.GET.get('page')
    try:
        tournaments_list = paginator.page(page)
    except PageNotAnInteger:
        tournaments_list = paginator.page(1)
    except EmptyPage:
        tournaments_list = paginator.page(paginator.num_pages)
    history = False
    return render_to_response("AlkoTurniej/my_tournaments_participant.html", {
        'user': request.user,
        'items': tournaments_list,
        'history': history
    }, RequestContext(request))


@login_required()
def my_tournaments_participant_history(request):
    user_participant = [i.tournament for i in TournamentParticipant.objects.filter(participant=request.user)]
    tournaments = Tournament.objects.filter(date__lte=datetime.date.today()).order_by("-date")
    tournaments = [i for i in tournaments if i in user_participant]
    paginator = Paginator(tournaments, 10)
    page = request.GET.get('page')
    try:
        tournaments_list = paginator.page(page)
    except PageNotAnInteger:
        tournaments_list = paginator.page(1)
    except EmptyPage:
        tournaments_list = paginator.page(paginator.num_pages)
    history = True
    return render_to_response("AlkoTurniej/my_tournaments_participant.html", {
        'user': request.user,
        'items': tournaments_list,
        'history': history
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
        form = self.form_class(request.POST, request.FILES)
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


@transaction.atomic
def tournament_site(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return render(request, "AlkoTurniej/tournament_does_not_exist.html")
    organizer = User.objects.get(username=tournament.organizer)
    if organizer == request.user:
        can_edit = True
    else:
        can_edit = False
    check_active(tournament_id)
    json_ladder = False
    if tournament.in_progress:
        json_ladder = create_json_ladder(tournament_id)
    return render(request, "AlkoTurniej/tournament.html",
                  {
                      'tournament': tournament,
                      'organizer': organizer,
                      'ladder': json_ladder,
                      'can_edit': can_edit
                  })


def create_json_ladder(tournament_id):
    result_json = []
    tournament = Tournament.objects.get(pk=tournament_id)
    tournament_encounters_first_round = Encounter.objects.filter(tournament=tournament_id, round=1)
    if len(tournament_encounters_first_round) > 0:
        for r in range(1, (int(log(tournament.current_participants, 2)) + 1)):
            round = []
            for i in range(0, int(tournament.current_participants / pow(2, r))):
                try:
                    encounter = Encounter.objects.get(tournament=tournament_id, round=r, encounter_id=i)
                except:
                    encounter = None
                if encounter is not None:
                    data = {"player1": {"name": encounter.user1.first_name + " " + encounter.user1.last_name,
                                        "id": encounter.user1.id},
                            "player2": {"name": encounter.user2.first_name + " " + encounter.user2.last_name,
                                        "id": encounter.user2.id}}
                else:
                    data = {"player1": {"name": "----", "id": -1},
                            "player2": {"name": "----", "id": -1}}
                round.append(data)
            result_json.append(round)
        round = []
        try:
            final = Encounter.objects.get(tournament=tournament_id, round=int(log(tournament.current_participants, 2)),
                                          encounter_id=0)
        except:
            final = None
        data = {"player1": {"name": "----", "id": -1}}
        if final is not None:
            if final.winner is not None:
                data = {"player1": {"name": final.winner.first_name + " " + final.winner.last_name,
                                    "id": final.winner.id}}
        round.append(data)
        result_json.append(round)
    return result_json  #


def check_active(tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if tournament.active:
        if tournament.deadline < datetime.date.today() or tournament.current_participants == tournament.max_participants:
            tournament.active = False
            if tournament.current_participants >= tournament.min_participants:
                tournament.in_progress = True
                generate_round(tournament_id)
            else:
                tournament.in_progress = False
                tournament.canceled = True
            tournament.save()


@transaction.atomic
@login_required()
def tournament_join(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        tournament = None
    if tournament is not None:
        if tournament.current_participants < tournament.max_participants and tournament.active:
            status = "ok"
        else:
            status = "not_active"
        if TournamentParticipant.objects.filter(tournament=tournament_id, participant=request.user).exists():
            status = "already_in"
    else:
        status = "wrong_tournament"
    if request.method == 'GET':
        form = TournamentParticipantForm(None)
        return render(request, "AlkoTurniej/join_tournament.html",
                      {
                          'status': status,
                          'form': form,
                          'tournament_id': tournament_id
                      })
    if request.method == 'POST':
        if status == "ok":
            form = TournamentParticipantForm(request.POST)
            if form.is_valid():
                license_number = form.cleaned_data["license_number"]
                ranking_position = form.cleaned_data["ranking_position"]
                tournament_participants = TournamentParticipant.objects.create(
                    tournament=Tournament.objects.get(pk=tournament_id),
                    participant=User.objects.get(username=request.user),
                    ranking_position=ranking_position,
                    license_number=license_number)
                tournament_participants.save()
                tournament = Tournament.objects.get(pk=tournament_id)
                tournament.current_participants = (tournament.current_participants + 1)
                tournament.save()
                return render(request, "AlkoTurniej/join_success.html")
        return render(request, "AlkoTurniej/join_tournament.html",
                      {
                          'status': status,
                          'form': form,
                          'tournament_id': tournament_id
                      })


def encounters(request):
    encounters_list = Encounter.objects.filter((Q(user1=request.user) | Q(user2=request.user)) & Q(winner=None))
    paginator = Paginator(encounters_list, 10)
    page = request.GET.get('page')
    try:
        encounters_list_page = paginator.page(page)
    except PageNotAnInteger:
        encounters_list_page = paginator.page(1)
    except EmptyPage:
        encounters_list_page = paginator.page(paginator.num_pages)
    return render(request, "AlkoTurniej/encounters.html",
                  {
                      'items': encounters_list_page
                  })


def winner_decision(request, encounter_id, decision):
    try:
        encounter = Encounter.objects.get(pk=encounter_id)
    except:
        encounter = None
    if encounter is not None:
        if encounter.winner is None:
            if request.user == encounter.user1:
                if decision == '1':
                    encounter.user1_decision_winner = True
                else:
                    encounter.user1_decision_winner = False
                if encounter.user2_decision_winner is not None:
                    if (encounter.user2_decision_winner == True) and (encounter.user1_decision_winner == False):
                        # user2 win
                        state = "loss"
                        encounter.winner = encounter.user2
                    elif (encounter.user1_decision_winner == True) and (encounter.user2_decision_winner == False):
                        # user1 win
                        state = "win"
                        encounter.winner = encounter.user1
                    else:
                        state = "non-compliance"
                        encounter.user1_decision_winner = None
                        encounter.user2_decision_winner = None
                else:
                    state = "wait"
            if request.user == encounter.user2:
                if decision == '1':
                    encounter.user2_decision_winner = True
                else:
                    encounter.user2_decision_winner = False
                if encounter.user1_decision_winner is not None:
                    if (encounter.user2_decision_winner == True) and (encounter.user1_decision_winner == False):
                        # user2 win
                        state = "win"
                        encounter.winner = encounter.user2
                    elif (encounter.user1_decision_winner == True) and (encounter.user2_decision_winner == False):
                        # user1 win
                        state = "loss"
                        encounter.winner = encounter.user1
                    else:
                        state = "non-compliance"
                        encounter.user1_decision_winner = None
                        encounter.user2_decision_winner = None
                else:
                    state = "wait"
            encounter.save()
            if (state == "loss") or (state == "win"):
                generate_next_encounter(encounter_id)
            return render(request, "AlkoTurniej/encounter_winner.html",
                          {
                              'state': state
                          })
    return render(request, "AlkoTurniej/encounter_winner.html",
                  {
                      'state': "wrong_encounter"
                  })


def generate_next_encounter(encounter_id):
    encounter = Encounter.objects.get(pk=encounter_id)
    size_of_round = encounter.tournament.current_participants / pow(2, encounter.round)
    print("id")
    print(encounter.encounter_id)
    print("size of round")
    print(size_of_round)
    if size_of_round == 1:
        return
    enemy_encounter_id = ((size_of_round - encounter.encounter_id) - 1)
    print("id2")
    print(enemy_encounter_id)
    try:
        enemy_encounter = Encounter.objects.get(encounter_id=enemy_encounter_id, round=encounter.round,
                                                tournament=encounter.tournament)
    except:
        enemy_encounter = None
    if enemy_encounter is not None:
        if enemy_encounter.winner is not None:
            id = min(enemy_encounter.encounter_id, encounter.encounter_id)
            if enemy_encounter.encounter_id % 2 == 1:
                new_encounter = Encounter.objects.create(
                    tournament=enemy_encounter.tournament,
                    round=enemy_encounter.round + 1,
                    encounter_id=id,
                    user1=encounter.winner,
                    user2=enemy_encounter.winner
                )
                new_encounter.save()
            else:
                new_encounter = Encounter.objects.create(
                    tournament=enemy_encounter.tournament,
                    round=enemy_encounter.round + 1,
                    encounter_id=id,
                    user1=enemy_encounter.winner,
                    user2=encounter.winner
                )
                new_encounter.save()


def generate_round(tournament_id):
    participants = [i.participant for i in
                    TournamentParticipant.objects.filter(tournament=tournament_id).order_by("ranking_position")]
    for i in range(0, int(len(participants) / 2)):
        encounter = Encounter.objects.create(
            tournament=Tournament.objects.get(pk=tournament_id),
            round=1,
            encounter_id=i,
            user1=User.objects.get(username=participants[i]),
            user2=User.objects.get(username=participants[(len(participants) - i) - 1])
        )
        encounter.save()
    tournament = Tournament.objects.get(pk=tournament_id)
    tournament.active = False
    tournament.save()


@login_required
def edit_tournament(request, tournament_id=None, template_name='AlkoTurniej/edit_tournament.html'):
    if id:
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        if tournament.organizer != request.user:
            return HttpResponseForbidden()
    else:
        tournament = Tournament(author=request.user)

    form = TournamentForm(request.POST or None, instance=tournament)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_tournaments_organizer'))

    return render_to_response(template_name, {
        'user': request.user,
        'form': form,
    }, context_instance=RequestContext(request))
