from django.conf.urls import url
from .views import Index, NewTournament, my_tournaments_organizer, my_tournaments_organizer_history, \
    my_tournaments_participant, tournament_site, tournament_join, my_tournaments_participant_history, encounters, \
    winner_decision, edit_tournament

urlpatterns = [
    url(r'^AlkoTurniej/$', Index.as_view(), name='index'),
    url(r'^$', Index.as_view(), name='blank'),
    url(r'^AlkoTurniej/organizuje/historia', my_tournaments_organizer_history, name='my_tournaments_organizer_history'),
    url(r'^AlkoTurniej/organizuje', my_tournaments_organizer, name='my_tournaments_organizer'),
    url(r'^AlkoTurniej/uczestnicze/historia', my_tournaments_participant_history,
        name='my_tournaments_participant_history'),
    url(r'^AlkoTurniej/uczestnicze', my_tournaments_participant, name='my_tournaments_participant'),
    url(r'^AlkoTurniej/nowy_turniej', NewTournament.as_view(), name='new_tournament'),
    url(r'^AlkoTurniej/edytuj_turniej/(?P<tournament_id>[0-9]+)', edit_tournament, name='edit_tournament'),
    url(r'^AlkoTurniej/turniej/(?P<tournament_id>[0-9]+)', tournament_site, name='tournament_site'),
    url(r'^AlkoTurniej/aplikuj/(?P<tournament_id>[0-9]+)', tournament_join, name='tournament_join'),
    url(r'^AlkoTurniej/pojedynki', encounters, name='encounters'),
    url(r'^AlkoTurniej/wynik/(?P<encounter_id>[0-9]+)/(?P<decision>[0-9]+)/', winner_decision, name='decision'),
]
