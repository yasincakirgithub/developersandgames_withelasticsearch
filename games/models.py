import datetime
from django.db import models
from django.contrib.auth.models import User


class Developer(models.Model):
    username = models.CharField(max_length=100)
    full_name = models.CharField(default="", max_length=200, null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'


class Game(models.Model):
    creator = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(default="", max_length=200, null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
