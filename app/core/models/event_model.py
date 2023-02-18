from django.db import models


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
    date = models.DateField()
    picture = models.ImageField(upload_to="events", blank=True, null=True)
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

    def __str__(self) -> str:
        return self.name
