from django import forms
from .models import Profile, Character, Item

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'name', 'essence_count']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['top_down_photo', 'name', 'character_class', 'level', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'bio']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'name', 'description']
