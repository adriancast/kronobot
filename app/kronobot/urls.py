from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from home.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prometheus/', include('django_prometheus.urls')),
    path('', index, name="index")

]

if settings.DEBUG:
    # When you are using the dev docker-compose, you need to serve the media files somehow
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
