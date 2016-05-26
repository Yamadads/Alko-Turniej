from django.contrib import admin
from django.conf.urls import include, url
# from AI.AlkoTurniej.forms import MyExtendedForm
# from registration.backends.default.views import RegistrationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^AlkoTurniej/', include('AlkoTurniej.urls')),
    url(r'^', include('AlkoTurniej.urls')),
    url(r'^accounts/', include('AlkoTurniej.urls_accounts'))
]