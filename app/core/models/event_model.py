from django.db import models

class EventModel(models.Model):
    name = models.CharField(max_length=256)
    date = models.DateField()
    kronolive_times_url = models.CharField(max_length=512)
    kronolive_inscribed_url = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
