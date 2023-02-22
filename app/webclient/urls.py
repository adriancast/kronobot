from .views import showcase
from django.urls import path
from webclient.views import events
from webclient.views import competitors


urlpatterns = [
    path("", showcase, name="index"),
    path("/archive/<int:year>", showcase, name="archive"),
    path('/events/<int:event_id>',events,name="event"),
    path('/competitors/<int:competitor_id>', competitors, name="competitors"),
    
    
]
