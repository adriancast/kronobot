from .views import showcase
from django.urls import path
from webclient.views import events
from webclient.views import competitors
from webclient.views import historic

urlpatterns = [
    path("", showcase, name="index"),
    path('archive/<int:year>',historic,name="archive"),
    path('events/<int:event_id>',events,name="event"),
    path('competitors/<int:competitor_id>',competitors,name="competitors"),
    
    
]
