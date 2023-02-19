from .views import showcase
from django.urls import path

urlpatterns = [
    path("", showcase, name="index"),
    path("/archive/<int:year>/", showcase, name="archive"),
]