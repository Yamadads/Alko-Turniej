from django.conf.urls import url
from django.contrib.auth import views
from .views import RegistrationView, index, new_tournament, my_tournaments, LoginView, logout_view

urlpatterns = [
    # url(r'^accounts/register/$', views.UserProfileRegistration.as_view(), name='registration_register'),
    url(r'^register', RegistrationView.as_view(), name='registration_register'),
    url(r'^login', LoginView.as_view(), name='auth_login'),
    url(r'^logout', logout_view, name='auth_logout'),
    url(r'^password_reset', LoginView.as_view(), name='auth_password_reset'),
    url(r'^password_change', LoginView.as_view(), name='auth_password_change'),
]
