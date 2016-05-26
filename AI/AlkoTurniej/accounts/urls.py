from django.conf.urls import url
from .views import RegistrationView, LoginView, logout_view, activate_view

urlpatterns = [
    url(r'^register', RegistrationView.as_view(), name='registration_register'),
    url(r'^activation_complete/(?P<activation_key_link>\w+)', activate_view, name='registration_activate'),
    url(r'^login', LoginView.as_view(), name='auth_login'),
    url(r'^logout', logout_view, name='auth_logout'),
    url(r'^password_reset', LoginView.as_view(), name='auth_password_reset'),
    url(r'^password_change', LoginView.as_view(), name='auth_password_change'),

]
