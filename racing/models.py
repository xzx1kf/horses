from django.db import models


class Meeting(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Horse(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=200)
    meeting = models.ForeignKey(Meeting)
    date = models.DateTimeField('date')
    horses = models.ManyToManyField(Horse)

    def __str__(self):
        return self.name
