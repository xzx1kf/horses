from django.db import models


class Meeting(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Horse(models.Model):
    forecast = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    last_run = models.IntegerField(default=0)
    name     = models.CharField(max_length=200)
    number   = models.IntegerField(default=0)
    weight   = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Race(models.Model):
    date     = models.DateTimeField()
    distance = models.IntegerField(default=0)
    going    = models.CharField(max_length=50)
    horses   = models.ManyToManyField(Horse)
    meeting  = models.ForeignKey(Meeting)
    name     = models.CharField(max_length=200)
    runners  = models.IntegerField(default=0)

    def __str__(self):
        return self.name
