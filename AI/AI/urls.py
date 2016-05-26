from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^AlkoTurniej/', include('AlkoTurniej.urls')),
    url(r'^', include('AlkoTurniej.urls')),
    url(r'^accounts/', include('AlkoTurniej.accounts.urls'))
]
