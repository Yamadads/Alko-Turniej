from django.conf.urls import url
from .views import index, new_tournament, my_tournaments

urlpatterns = [
    url(r'^AlkoTurniej/$', index, name='index'),
    url(r'^$', index, name='blank'),
    url(r'^AlkoTurniej/moje_turnieje', my_tournaments, name='my_tournaments'),
    url(r'^AlkoTurniej/nowy_turniej', new_tournament, name='new_tournament'),
]
