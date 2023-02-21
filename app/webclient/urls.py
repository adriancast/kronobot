from .views import showcase
from django.urls import path
from webclient.views import events


urlpatterns = [
    path("", showcase, name="index"),
    path("/archive/<int:year>/", showcase, name="archive"),
    path('events',events,name="events")
    
]
