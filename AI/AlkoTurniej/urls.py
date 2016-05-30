from django.conf.urls import url
from .views import index, new_tournament_form, my_tournaments, tournament_site

urlpatterns = [
    url(r'^AlkoTurniej/$', index, name='index'),
    url(r'^$', index, name='blank'),
    url(r'^AlkoTurniej/moje_turnieje', my_tournaments, name='my_tournaments'),
    url(r'^AlkoTurniej/nowy_turniej', new_tournament_form, name='new_tournament'),
    url(r'^AlkoTurniej/turniej/(?P<tournament_id>[0-9]+)', tournament_site, name='tournament_site'),
]
