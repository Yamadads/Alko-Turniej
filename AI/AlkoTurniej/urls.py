from django.conf.urls import url
from django.contrib.auth import views
from .views import RegistrationView, index, new_tournament, my_tournaments, LoginView, logout_view

urlpatterns = [
    # url(r'^accounts/register/$', views.UserProfileRegistration.as_view(), name='registration_register'),
    url(r'^AlkoTurniej/$', index, name='index'),
    url(r'^$', index, name='blank'),
    url(r'^AlkoTurniej/moje_turnieje', my_tournaments, name='my_tournaments'),
    url(r'^AlkoTurniej/nowy_turniej', new_tournament, name='new_tournament'),
]
