from django.conf.urls import url
from .views import RegistrationView, LoginView, logout_view, activate_view, ChangePasswordView

urlpatterns = [
    url(r'^register', RegistrationView.as_view(), name='registration_register'),
    url(r'^activation_complete/(?P<activation_key_link>\w+)', activate_view, name='registration_activate'),
    url(r'^login', LoginView.as_view(), name='auth_login'),
    url(r'^logout', logout_view, name='auth_logout'),
    url(r'^reset_password', LoginView.as_view(), name='auth_password_reset'),
    url(r'^change_password', ChangePasswordView.as_view(), name='auth_password_change'),

]
