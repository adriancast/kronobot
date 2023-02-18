from django.db import models


class EventCategory(models.TextChoices):
    RALLY = "RALLY"
    HILL_CLIMB = "HILL-CLIMB"
    AUTO_CROSS = "AUTO-CROSS"
    KARTING = "KARTING"

class EventModel(models.Model):
    name = models.CharField(max_length=256)
    date = models.DateField()
    picture = models.ImageField(upload_to='events', blank=True, null=True)
    category = models.CharField(
        max_length=16,
        choices=EventCategory.choices,
        default=EventCategory.RALLY,
    )
    kronolive_times_url = models.CharField(max_length=512)
    kronolive_inscribed_url = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
