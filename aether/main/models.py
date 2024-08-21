# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    essence_count = models.IntegerField(default=0)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username  # Set the default name to the usernamee


# This is the model for the stuff that can appear on the homepage on specific days
class SeasonalContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title