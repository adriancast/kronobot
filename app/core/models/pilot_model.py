from django.db import models


class CompetitorModel(models.Model):
    name = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='cars')

    def __str__(self):
        return self.name
