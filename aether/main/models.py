# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)



class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    participants = models.ManyToManyField(User, related_name='events_participated', blank=True)

    def __str__(self):
        return self.title



# This is the model for the stuff that can appear on the homepage on specific days
class SeasonalContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    

## FROM INVENTORY TEST

class Item(models.Model):
    item_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    set = models.ForeignKey('Set', on_delete=models.CASCADE, related_name='items_in_set', blank=True, null=True)

    def __str__(self):
        return self.item_name or 'Unnamed Item'

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_name = models.CharField(max_length=100, blank=True)
    essence_count = models.IntegerField(default=0)
    characters = models.ManyToManyField('Character', related_name='profiles_with_character', blank=True)

    def __str__(self):
        return self.user.username  # Adjusted to use username

    def save(self, *args, **kwargs):
        # Set profile_name to username if it's empty
        if not self.profile_name:
            self.profile_name = self.user.username
        super().save(*args, **kwargs)


class ProfileItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='profile_items')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'item')

    def __str__(self):
        return f"{self.item.item_name} ({self.quantity})"

class Character(models.Model):
    character_name = models.CharField(max_length=100, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='character_profiles', blank=True, null=True)
    # Stats
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    level = models.IntegerField()
    character_class = models.TextField(blank=True, null=True)

    top_down_photo = models.ImageField(upload_to='characters/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.character_name or 'Unnamed Character'

class Set(models.Model):
    set_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item, related_name='sets_containing_item', blank=True)

    def __str__(self):
        return self.set_name or 'Unnamed Set'

class Bundle(models.Model):
    bundle_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sets = models.ManyToManyField(Set, related_name='bundles_containing_set', blank=True)

    def __str__(self):
        return self.bundle_name or 'Unnamed Bundle'


class ShopItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()  # Price in essence

    def __str__(self):
        return f"{self.item.item_name} - {self.price} essence"
