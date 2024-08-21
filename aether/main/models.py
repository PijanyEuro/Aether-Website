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