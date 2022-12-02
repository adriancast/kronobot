from django.db import models


class SectionModel(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    event = models.ForeignKey("EventModel", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
