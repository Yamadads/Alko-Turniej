from django.conf.urls import url
from .views import index, NewTournament, my_tournaments_organizer, my_tournaments_participant, tournament_site

urlpatterns = [
    url(r'^AlkoTurniej/$', index, name='index'),
    url(r'^$', index, name='blank'),
    url(r'^AlkoTurniej/organizuje', my_tournaments_organizer, name='my_tournaments_organizer'),
    url(r'^AlkoTurniej/uczestnicze', my_tournaments_participant, name='my_tournaments_participant'),
    url(r'^AlkoTurniej/nowy_turniej', NewTournament.as_view(), name='new_tournament'),
    url(r'^AlkoTurniej/turniej/(?P<tournament_id>[0-9]+)', tournament_site, name='tournament_site'),
]
