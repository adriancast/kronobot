from django.db import models
from datetime import date
from ckeditor.fields import RichTextField 

class EventCategory(models.TextChoices):
    RALLY = "RALLY"
    HILL_CLIMB = "HILL-CLIMB"
    AUTO_CROSS = "AUTO-CROSS"
    KARTING = "KARTING"


class EventProvider(models.TextChoices):
    KRONOLIVE = "KRONOLIVE"
    KRONOBOT = "KRONOBOT"


class EventModel(models.Model):
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    picture = models.ImageField(upload_to="events", blank=True, null=True)
    description = RichTextField(blank=True)
    category = models.CharField(
        max_length=16,
        choices=EventCategory.choices,
    )
    provider_name = models.CharField(
        max_length=16,
        choices=EventProvider.choices,
        default=EventProvider.KRONOBOT
    )
    provider_data = models.JSONField(default=dict, blank=True)

    def is_live(self):
        return self.start_date <= date.today() <= self.end_date


    def __str__(self) -> str:
        return self.name
