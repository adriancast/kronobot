from django.db import models


class SectionTimeModel(models.Model):
    section = models.ForeignKey("SectionModel", on_delete=models.CASCADE)
    inscription = models.ForeignKey("InscriptionModel", on_delete=models.CASCADE)
    section_time = models.DurationField()

    class Meta:
        unique_together = ("section", "inscription", "section_time")

    def __str__(self):
        return self.section.name
