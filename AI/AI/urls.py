from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^AlkoTurniej/', include('AlkoTurniej.urls')),
    url(r'^', include('AlkoTurniej.urls')),
    url(r'^accounts/', include('AlkoTurniej.accounts.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)