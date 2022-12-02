from typing import Optional

from django.db import models


class InscriptionModel(models.Model):
    car = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    dorsal = models.CharField(max_length=16)
    event = models.ForeignKey("EventModel", on_delete=models.CASCADE)
    pilot = models.ForeignKey("CompetitorModel", on_delete=models.CASCADE, related_name="pilot_inscription")
    copilot = models.ForeignKey("CompetitorModel", on_delete=models.CASCADE, related_name="copilot_inscription", null=True, blank=True)

    def car_image(self) -> Optional[str]:
        if self.pilot.photo:
            return self.pilot.photo.url.replace("/mediafiles", "mediafiles")

    def __str__(self):
        return self.car
